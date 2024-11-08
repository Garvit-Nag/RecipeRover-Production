'use client';

import { Spotlight } from "./ui/Spotlight";
import Link from "next/link";
import { Button } from "./ui/moving-border";

function HeroSection() {
    return (
        <div 
            className="h-auto md:h-[49.3rem] w-full rounded-md flex flex-col items-center justify-center relative overflow-hidden mx-auto py-10 md:py-0"
            style={{
                backgroundImage: `url('/bghai.png')`,
                backgroundSize: 'cover',
                backgroundPosition: 'center',
            }}
        >
            <div className="absolute inset-0 z-0">
                <div className="absolute top-0 left-0 right-0 bg-gradient-to-b from-black to-transparent"></div>
                <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-black to-transparent"></div>
            </div>
            {/* <Spotlight
                className="-top-40 left-0 md:left-60 md:-top-20"
                fill="white"
            /> */}
            <div className="p-4 relative z-10 w-full text-center">
                <h1 className="mt-20 md:mt-0 text-4xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400">
                    Master the Recipe Art 
                </h1>
                <br />
                <p className="mt-4 font-normal text-base md:text-lg text-neutral-300 max-w-lg mx-auto">
                    Welcome to 'RecipeRover,' we all relish indulging in great dishes, but how many of us take pleasure in watching recipes unfold? Here, we aim to bring you the finest and most popular recipes from around the globe, making it effortless to find that perfect dish without the hassle.
                </p>
                <div className="mt-4">
                    <Link href={'/form'}>
                        <Button borderRadius="1.7rem" className="bg-black dark:bg-black text-white dark:text-white">
                            Explore Recipes 
                        </Button>
                    </Link>
                </div>
            </div>
        </div>
    );
}

export default HeroSection;