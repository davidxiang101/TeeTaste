const LoadingComponent = () => {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen w-full bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-sky-400 to-indigo-900 text-zinc-200">
            <div className="spinner w-9 h-9"></div>
            <p className="font-zinc-200 mt-2 text-zinc-200">Fetching shoes...</p>
        </div>
    );
};

export default LoadingComponent;
