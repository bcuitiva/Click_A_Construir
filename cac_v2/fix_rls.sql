-- ══════════════════════════════════════════════════════════════════
-- FIX: Error RLS al registrarse
-- Ejecutar en Supabase → SQL Editor → New Query → Run
-- ══════════════════════════════════════════════════════════════════

-- 1. Permitir que el trigger (que corre como service role) inserte el perfil
DROP POLICY IF EXISTS "Insertar perfil propio" ON public.users;
CREATE POLICY "Insertar perfil propio" ON public.users
  FOR INSERT WITH CHECK (true);

-- 2. Recrear el trigger con SECURITY DEFINER para que bypass RLS
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.users (id, email, name, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'name', 'Usuario'),
    COALESCE(NEW.raw_user_meta_data->>'role', 'cliente')
  )
  ON CONFLICT (id) DO NOTHING;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = public;

-- 3. Recrear el trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 4. Verificar que las políticas básicas estén bien
DROP POLICY IF EXISTS "Ver perfiles" ON public.users;
CREATE POLICY "Ver perfiles" ON public.users
  FOR SELECT USING (true);

DROP POLICY IF EXISTS "Editar mi perfil" ON public.users;
CREATE POLICY "Editar mi perfil" ON public.users
  FOR UPDATE USING (auth.uid() = id);
