-- ══════════════════════════════════════════════════════════════════
-- FIX: Error RLS en Storage (foto de perfil e imágenes de proyectos)
-- Ejecutar en Supabase → SQL Editor → New Query → Run
-- ══════════════════════════════════════════════════════════════════

-- 1. Crear los buckets si no existen
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true)
ON CONFLICT (id) DO UPDATE SET public = true;

INSERT INTO storage.buckets (id, name, public)
VALUES ('project-images', 'project-images', true)
ON CONFLICT (id) DO UPDATE SET public = true;

-- 2. Políticas para el bucket "avatars"
DROP POLICY IF EXISTS "Avatars son públicos"       ON storage.objects;
DROP POLICY IF EXISTS "Cualquiera puede subir avatar" ON storage.objects;
DROP POLICY IF EXISTS "Dueño puede actualizar avatar" ON storage.objects;
DROP POLICY IF EXISTS "Dueño puede eliminar avatar"   ON storage.objects;

CREATE POLICY "Avatars publicos lectura"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Avatars subida autenticados"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'avatars');

CREATE POLICY "Avatars actualizar"
  ON storage.objects FOR UPDATE
  USING (bucket_id = 'avatars');

CREATE POLICY "Avatars eliminar"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'avatars');

-- 3. Políticas para el bucket "project-images"
CREATE POLICY "ProjectImages publicos lectura"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'project-images');

CREATE POLICY "ProjectImages subida"
  ON storage.objects FOR INSERT
  WITH CHECK (bucket_id = 'project-images');

CREATE POLICY "ProjectImages actualizar"
  ON storage.objects FOR UPDATE
  USING (bucket_id = 'project-images');

CREATE POLICY "ProjectImages eliminar"
  ON storage.objects FOR DELETE
  USING (bucket_id = 'project-images');
