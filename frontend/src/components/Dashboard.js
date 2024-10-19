import React from 'react';
import '../styles/styles.css'; 

const DashboardContent = () => {
    return (
        <div className="bg-gradient-to-r from-[#0a0034] to-[#180046] min-h-screen p-8 text-white">
            {/* Dashboard Header */}
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
    );
};

export default DashboardContent;