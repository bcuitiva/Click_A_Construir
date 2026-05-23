-- ══════════════════════════════════════════════════════════════════
-- Agregar redes sociales a la tabla users
-- Ejecutar en Supabase → SQL Editor → New Query → Run
-- ══════════════════════════════════════════════════════════════════

ALTER TABLE public.users
  ADD COLUMN IF NOT EXISTS instagram  text,
  ADD COLUMN IF NOT EXISTS facebook   text,
  ADD COLUMN IF NOT EXISTS whatsapp   text,
  ADD COLUMN IF NOT EXISTS website    text;
