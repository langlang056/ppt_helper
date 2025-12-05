import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "UniTutor AI - 智能课件讲解助手",
  description: "将复杂的大学讲义转化为通俗易懂的中文解释",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}
