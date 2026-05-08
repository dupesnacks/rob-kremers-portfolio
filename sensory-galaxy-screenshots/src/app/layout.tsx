import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sensory Galaxy Screenshots",
  description: "App screenshot framing tool",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, background: "#f5f5f5", fontFamily: "system-ui, sans-serif" }}>
        {children}
      </body>
    </html>
  );
}
