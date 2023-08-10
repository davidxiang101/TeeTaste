const LoadingComponent = () => {
    return (
        <div className="flex flex-col items-center justify-center">
            <div className="spinner w-9 h-9"></div>
            <p className="font-slate-100 mt-2 text-gray-500">Loading...</p>
        </div>
    );
};

export default LoadingComponent;
