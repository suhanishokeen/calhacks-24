import React, { useState } from 'react';
import '../styles/styles.css'; 

const DashboardContent = () => {
    const [isSidebarOpen, setSidebarOpen] = useState(false);

    // Toggle Sidebar
    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="relative bg-gradient-to-r from-[#0a0034] to-[#180046] min-h-screen p-8 text-white">
            
            {/* Hamburger Menu (Three Bars) */}
            <div className="absolute top-4 left-4 cursor-pointer z-50" onClick={toggleSidebar}>
                <div className="w-8 h-1 bg-white mb-1"></div>
                <div className="w-8 h-1 bg-white mb-1"></div>
                <div className="w-8 h-1 bg-white"></div>
            </div>

            {/* Sidebar */}
            <div className={`fixed top-0 left-0 h-full bg-[#1e1e4d] p-6 transform ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 z-40 shadow-lg`}>
                <h2 className="text-3xl font-semibold mb-6">Menu</h2>
                <ul className="text-white text-lg">
                    <li className="mb-4">
                        <a href="/ai-friend" className="hover:text-gray-400 transition">AI Friend</a>
                    </li>
                    <li className="mb-4">
                        <a href="/tables" className="hover:text-gray-400 transition">Tables</a>
                    </li>
                    <li className="mb-4">
                        <a href="/account" className="hover:text-gray-400 transition">Account Pages</a>
                    </li>
                    <li className="mb-4">
                        <a href="/profile" className="hover:text-gray-400 transition">Profile</a>
                    </li>
                    <li className="mb-4">
                        <a href="/logout" className="hover:text-gray-400 transition">Logout</a>
                    </li>
                </ul>
            </div>

            {/* Main Dashboard Content (Widgets) */}
            <div className={`transition-opacity duration-300 ${isSidebarOpen ? 'opacity-50' : 'opacity-100'}`}>
                <header className="flex justify-between items-center mb-8">
                    <h1 className="text-4xl font-bold">Dashboard</h1>
                    <input
                        type="text"
                        placeholder="Type here..."
                        className="p-2 rounded-md bg-[#2a2a72] text-white"
                    />
                </header>

                {/* Dashboard Grid Layout */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    
                    {/* AI Friend Section */}
                    <div className="bg-[#25135a] p-6 rounded-lg shadow-lg flex flex-col justify-between">
                        <div>
                            <h2 className="text-2xl font-semibold mb-4">AI Friend</h2>
                            <p className="text-gray-400">Ask me anything!</p>
                        </div>
                        <button className="custom-button">
                            Tap to record
                        </button>
                    </div>

                    {/* Tables Section */}
                    <div className="bg-[#25135a] p-6 rounded-lg shadow-lg">
                        <h2 className="text-2xl font-semibold mb-4">Tables</h2>
                    </div>

                    {/* Account Pages Section */}
                    <div className="bg-[#25135a] p-6 rounded-lg shadow-lg">
                        <h2 className="text-2xl font-semibold mb-4">Account Pages</h2>
                        <ul className="text-gray-400">
                            <li className="mb-2">
                                <a href="/profile" className="hover:text-white transition">Profile</a>
                            </li>
                            <li className="mb-2">
                                <a href="/logout" className="hover:text-white transition">Logout</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DashboardContent;
