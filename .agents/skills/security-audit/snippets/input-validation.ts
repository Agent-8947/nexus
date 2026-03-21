import { z } from 'zod';

export const schemas = {
  userId: z.string().uuid('Invalid user ID format'),
  email: z.string().email().max(255).transform(e => e.toLowerCase().trim()),
  password: z.string().min(8).max(128).regex(/[a-z]/).regex(/[A-Z]/).regex(/[0-9]/),
  safeUrl: z.string().url().refine((url) => {
    const parsed = new URL(url);
    const blocked = ['localhost', '127.0.0.1', '169.254.'];
    return !blocked.some(b => parsed.hostname.startsWith(b));
  }, 'URL not allowed'),
};

export function validateBody<T>(schema: z.ZodSchema<T>) {
  return async (request: Request) => {
    try {
      const body = await request.json();
      return { data: schema.parse(body) };
    } catch (error) {
      return { error: 'Validation failed', details: error };
    }
  };
}
