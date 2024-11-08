'use client'
import React from 'react'
import { InfiniteMovingCards } from "./ui/infinite-moving-cards";

const testimonials = [
      {
        quote: "The melody of a dish lies in the harmony of its ingredients, where each note contributes to the symphony of flavors.",
        name: "Massimo Bottura",
        title: "Osteria Francescana",
      },
      {
        quote: "To cook, or not to cook, that is never the question: for in the kitchen, creation is inevitable. Whether in the heat of the moment or the calm of preparation, harmony always finds its way to the plate.",
        name: "Gordon Ramsay",
        title: "Hell's Kitchen",
      },
      {
        quote: "All that we taste or savor is but a flavor within a flavor, layering itself into an unforgettable dish.",
        name: "Dominique Crenn",
        title: "Atelier Crenn",
      },
      {
        quote: "It is a truth universally acknowledged, that a chef in possession of a good palate, must be in want of a dish to create.",
        name: "Yotam Ottolenghi",
        title: "Plenty",
      },
      {
        quote: "Call me René. Some years ago—never mind how long precisely—having tasted flavors from all corners of the world, I thought I would explore the essence of the earth on my plate.",
        name: "René Redzepi",
        title: "Noma",
      },      
  ];  

function InstructionTestimonialCards() {
  return (
    <div className='h-[28rem] w-full bg-black bg-grid-white/[0.2] relative flex flex-col items-center justify-center overflow-hidden font-fira'>
        <h2 className='text-center text-3xl font-bold text-white mb-8 z-10'>Hear the Symphony of Cooking</h2>
        <div className='flex justify-center w-full overflow-hidden px-4 sm:px-6 lg:px-8'>
            <div className='w-full max-w-6xl'>
            <InfiniteMovingCards
                items={testimonials}
                direction="right"
                speed="slow"
            />
            </div>
        </div>
    </div>
  )
}

export default InstructionTestimonialCards