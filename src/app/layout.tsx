import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import "@copilotkit/react-ui/styles.css";
import { ThemeProvider } from "@/components/theme-provider";
import { FronteggAppProvider } from "@frontegg/nextjs/app";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Demo Viewer by CopilotKit",
  description: "Demo Viewer by CopilotKit",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const authOptions = {
    keepSessionAlive: true, // Uncomment this in order to maintain the session alive
  };

  return (
    <html
      lang="en"
      suppressHydrationWarning
    >
      <body className={`${geistSans.variable} ${geistMono.variable} antialiased`}>
        <FronteggAppProvider
          authOptions={authOptions}
          hostedLoginBox={true}
        >
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {children}
          </ThemeProvider>
        </FronteggAppProvider>
      </body>
    </html>
  );
}
