import React from "react"

import { ToastContainer} from 'react-toastify';
import { useServer } from "@/pages/_server";

export default function Layout({ children }: { children: React.ReactNode }) {
    const layout = useServer();
    return (
        <>
            <ToastContainer />
            <div className="flex justify-center items-center min-h-screen bg-base-200">
                <div className="w-full max-w-4xl p-6 bg-base-100 rounded-xl shadow-lg">
                    {layout.user?.email ? (
                        <div className="flex justify-end mb-4">
                            <button 
                                className="btn btn-secondary"
                                onClick={() => {layout.logout() ; window.location.href = '/login'}}
                            >
                                Logout
                            </button>
                        </div>
                    ) : (
                        <div className="flex justify-end mb-4">
                            <a 
                                className="btn btn-primary"
                                href="/login"
                            >
                                Login
                            </a>
                        </div>
                    )}
                    {children}
                </div>
            </div>
        </>
    )
}