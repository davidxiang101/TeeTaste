const LoadingComponent = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full bg-gradient-to-br to-80% from-blue-700 to-purple-800 text-zinc-200">
            <div className="spinner w-9 h-9"></div>
            <p className="font-zinc-200 mt-2 text-zinc-200">Fetching shoes...</p>
        </div>
    );
};

export default LoadingComponent;
