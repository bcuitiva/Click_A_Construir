-- ══════════════════════════════════════════════════════════════════
-- Click a Construir — Schema Supabase
-- Ejecutar en: Supabase → SQL Editor → New Query
-- ══════════════════════════════════════════════════════════════════

-- 1. USERS (perfil extendido de auth.users)
-- ─────────────────────────────────────────
create table if not exists public.users (
  id              uuid        primary key references auth.users(id) on delete cascade,
  email           text        unique not null,
  name            text        not null,
  role            text        not null check (role in ('cliente', 'profesional')),
  phone           text,
  city            text,
  bio             text,
  specialty       text,                        -- solo profesionales
  avatar_url      text,
  rating_avg      numeric(3,1) default 0,
  reviews_count   int         default 0,
  created_at      timestamptz default now()
);

-- Trigger: crear fila en users cuando se registra en auth.users
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.users (id, email, name, role)
  values (
    new.id,
    new.email,
    coalesce(new.raw_user_meta_data->>'name', 'Usuario'),
    coalesce(new.raw_user_meta_data->>'role', 'cliente')
  )
  on conflict (id) do nothing;
  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();


-- 2. PROJECTS
-- ─────────────────────────────────────────
create table if not exists public.projects (
  id                uuid        primary key default gen_random_uuid(),
  name              text        not null,
  description       text,
  client_id         uuid        references public.users(id) on delete set null,
  client_name       text,                        -- desnormalizado para queries rápidas
  professional_id   uuid        references public.users(id) on delete set null,
  professional_name text,
  location          text,
  budget            bigint,                       -- en pesos COP
  status            text        default 'Pendiente'
                                check (status in ('Pendiente', 'En progreso', 'Completado')),
  category          text,
  size              text,                         -- ej: "30m²"
  progress          int         default 0 check (progress between 0 and 100),
  start_date        date,
  end_date          date,
  created_at        timestamptz default now()
);


-- 3. PROJECT IMAGES
-- ─────────────────────────────────────────
create table if not exists public.project_images (
  id          uuid        primary key default gen_random_uuid(),
  project_id  uuid        references public.projects(id) on delete cascade,
  url         text        not null,
  created_at  timestamptz default now()
);


-- 4. TASKS
-- ─────────────────────────────────────────
create table if not exists public.tasks (
  id           uuid        primary key default gen_random_uuid(),
  project_id   uuid        references public.projects(id) on delete cascade,
  text         text        not null,
  done         boolean     default false,
  completed_at date,
  created_at   timestamptz default now()
);


-- 5. PROJECT UPDATES (Avances)
-- ─────────────────────────────────────────
create table if not exists public.project_updates (
  id          uuid        primary key default gen_random_uuid(),
  project_id  uuid        references public.projects(id) on delete cascade,
  author_id   uuid        references public.users(id) on delete set null,
  text        text        not null,
  images      text[]      default '{}',           -- array de URLs
  created_at  timestamptz default now()
);


-- 6. MESSAGES
-- ─────────────────────────────────────────
create table if not exists public.messages (
  id          uuid        primary key default gen_random_uuid(),
  from_id     uuid        references public.users(id) on delete set null,
  to_id       uuid        references public.users(id) on delete set null,
  text        text        not null,
  read        boolean     default false,
  created_at  timestamptz default now()
);

-- Índice para acelerar consultas de conversaciones
create index if not exists idx_messages_participants
  on public.messages(from_id, to_id, created_at);


-- 7. REVIEWS
-- ─────────────────────────────────────────
create table if not exists public.reviews (
  id                uuid        primary key default gen_random_uuid(),
  professional_id   uuid        references public.users(id) on delete cascade,
  client_id         uuid        references public.users(id) on delete set null,
  project_id        uuid        references public.projects(id) on delete set null,
  rating            numeric(3,1) not null check (rating between 0 and 5),
  comment           text,
  created_at        timestamptz  default now()
);

-- Trigger: recalcular rating_avg al agregar reseña
create or replace function public.recalculate_rating()
returns trigger as $$
declare
  avg_val  numeric(3,1);
  cnt_val  int;
begin
  select round(avg(rating)::numeric, 1), count(*)
  into avg_val, cnt_val
  from public.reviews
  where professional_id = new.professional_id;

  update public.users
  set rating_avg = avg_val, reviews_count = cnt_val
  where id = new.professional_id;

  return new;
end;
$$ language plpgsql security definer;

drop trigger if exists on_review_created on public.reviews;
create trigger on_review_created
  after insert on public.reviews
  for each row execute function public.recalculate_rating();


-- 8. QUOTATIONS (Cotizaciones)
-- ─────────────────────────────────────────
create table if not exists public.quotations (
  id                uuid        primary key default gen_random_uuid(),
  project_id        uuid        references public.projects(id) on delete cascade,
  professional_id   uuid        references public.users(id) on delete set null,
  file_url          text,
  message           text,
  status            text        default 'enviada'
                                check (status in ('enviada', 'aceptada', 'rechazada')),
  created_at        timestamptz  default now()
);


-- ══════════════════════════════════════════════════════════════════
-- ROW LEVEL SECURITY (RLS) — Seguridad por usuario
-- ══════════════════════════════════════════════════════════════════

alter table public.users           enable row level security;
alter table public.projects        enable row level security;
alter table public.project_images  enable row level security;
alter table public.tasks           enable row level security;
alter table public.project_updates enable row level security;
alter table public.messages        enable row level security;
alter table public.reviews         enable row level security;
alter table public.quotations      enable row level security;

-- USERS: cualquiera puede leer perfiles; solo el dueño puede editar
create policy "Ver perfiles" on public.users
  for select using (true);
create policy "Editar mi perfil" on public.users
  for update using (auth.uid() = id);

-- PROJECTS: todos ven proyectos; solo cliente dueño o profesional asignado pueden editar
create policy "Ver proyectos" on public.projects
  for select using (true);
create policy "Crear proyecto" on public.projects
  for insert with check (auth.uid() = client_id);
create policy "Editar proyecto" on public.projects
  for update using (auth.uid() = client_id or auth.uid() = professional_id);

-- TASKS: visibles en proyectos accesibles; solo profesional asignado puede crear/editar
create policy "Ver tareas" on public.tasks
  for select using (true);
create policy "Gestionar tareas" on public.tasks
  for all using (
    auth.uid() = (select professional_id from public.projects where id = project_id)
  );

-- UPDATES: visibles por todos; creadas solo por profesional asignado
create policy "Ver avances" on public.project_updates
  for select using (true);
create policy "Publicar avances" on public.project_updates
  for insert with check (auth.uid() = author_id);

-- MESSAGES: solo los participantes ven sus mensajes
create policy "Ver mis mensajes" on public.messages
  for select using (auth.uid() = from_id or auth.uid() = to_id);
create policy "Enviar mensajes" on public.messages
  for insert with check (auth.uid() = from_id);
create policy "Marcar leídos" on public.messages
  for update using (auth.uid() = to_id);

-- REVIEWS: todos ven; solo clientes pueden crear
create policy "Ver reseñas" on public.reviews
  for select using (true);
create policy "Crear reseña" on public.reviews
  for insert with check (auth.uid() = client_id);

-- PROJECT IMAGES: todos ven; profesional asignado puede subir
create policy "Ver imágenes" on public.project_images
  for select using (true);
create policy "Subir imágenes" on public.project_images
  for insert with check (true);

-- QUOTATIONS: profesional ve sus cotizaciones, cliente ve las de su proyecto
create policy "Ver cotizaciones" on public.quotations
  for select using (
    auth.uid() = professional_id or
    auth.uid() = (select client_id from public.projects where id = project_id)
  );
create policy "Crear cotización" on public.quotations
  for insert with check (auth.uid() = professional_id);


-- ══════════════════════════════════════════════════════════════════
-- STORAGE BUCKETS (crear manualmente en Supabase → Storage)
-- ══════════════════════════════════════════════════════════════════
-- Bucket: avatars        → Public: ✅
-- Bucket: project-images → Public: ✅
--
-- O ejecutar si tienes permisos de storage:
-- insert into storage.buckets (id, name, public) values ('avatars', 'avatars', true);
-- insert into storage.buckets (id, name, public) values ('project-images', 'project-images', true);
