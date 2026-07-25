import './globals.css'; // This ensures your Tailwind styles are loaded!

export const metadata = {
    title: 'CloudRAG Explorer',
    description: 'AWS & Kubernetes RAG Assistant',
};

export default function RootLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <html lang="en">
            {/* The background color here matches your dark theme */}
            <body className="bg-slate-950 text-slate-200 antialiased">
                {children}
            </body>
        </html>
    );
}