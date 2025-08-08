import './globals.css';
import type { ReactNode } from 'react';

export const metadata = {
  title: 'XQuiz Super',
  description: 'Construtor de funis de quiz avançado',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body className="min-h-dvh bg-white text-slate-900">
        {children}
      </body>
    </html>
  );
}