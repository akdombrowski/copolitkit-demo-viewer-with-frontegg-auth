import { FronteggAppProvider } from "@frontegg/nextjs/app";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const authOptions = {
    keepSessionAlive: true, // Uncomment this in order to maintain the session alive
  };

  return (
    <html>
      <head></head>
      <body>
        <FronteggAppProvider
          authOptions={authOptions}
          hostedLoginBox={true}
        >
          {children}
        </FronteggAppProvider>
      </body>
    </html>
  );
}
