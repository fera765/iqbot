/// <reference types="next" />
/// <reference types="next/image-types/global" />

// Env types
declare namespace NodeJS {
  interface ProcessEnv {
    NEXT_PUBLIC_BASE_URL?: string;
  }
}