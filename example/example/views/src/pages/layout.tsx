import React from "react"
import { createServerPage } from "@/components/ServerPages";

import { ToastContainer} from 'react-toastify';
import { useServer } from "@/pages/_server";
import * as LayoutController from "./_server";

import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/react';

export const LayoutPage = createServerPage(LayoutController);

const AppBar = () => {
    const {user, logout} = LayoutPage.useContext();
    const userInitials = user ? `${user.email[0].toUpperCase()}` : "";

    return (
        <div className="flex-none p-4 bg-base-100 shadow-md">
            <div className="flex justify-between items-center">
                <div className="text-2xl font-bold"><a href="/">PollsApp</a></div>
                {user?.email ? (
                    <Menu as="div" className="relative">
                        <MenuButton className="btn btn-circle btn-secondary">
                            {userInitials}
                        </MenuButton>
                        <MenuItems className="absolute right-0 mt-2 w-48 bg-white shadow-lg z-10 rounded-md">
                            <MenuItem>
                                <a
                                    className="block px-4 py-2 text-sm text-gray-700 rounded-md"
                                    href="/admin"
                                >
                                    Admin
                                </a>
                            </MenuItem>
                            <MenuItem>
                                <button
                                    className="block w-full text-left px-4 py-2 text-sm text-gray-700 rounded-md"
                                    onClick={() => { logout(); window.location.href = '/login' }}
                                >
                                    Logout
                                </button>
                            </MenuItem>
                        </MenuItems>
                    </Menu>
                ) : (
                    <a 
                        className="btn btn-primary"
                        href="/login"
                    >
                        Login
                    </a>
                )}
            </div>
        </div>
    );
};

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
        <LayoutPage.Provider>
            <ToastContainer />
            <div className="flex flex-col min-h-screen">
                <AppBar />
                <div className="flex-grow flex justify-center items-center bg-base-200">
                    <div className="w-full max-w-4xl p-6 bg-base-100 rounded-xl shadow-lg">
                        {children}
                    </div>
                </div>
            </div>
        </LayoutPage.Provider>
    );
}