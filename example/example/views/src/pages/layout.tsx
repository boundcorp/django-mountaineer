import React from "react"

import "@/main.css"

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex justify-center items-center min-h-screen bg-base-200">
            <div className="w-full max-w-4xl p-6 bg-base-100 rounded-xl shadow-lg">
                {children}
            </div>
        </div>
    )
}