import React from 'react';
import styles from './SecondaryLoader.module.css';

const SecondaryLoader: React.FC = () => {
  return (
    <div className={`${styles.body} dark:bg-gray-900 dark:text-white`}>
      <main className={styles.main}>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="128px"
          width="256px"
          viewBox="0 0 256 128"
          className={styles.ip}
        >
          <defs>
            <linearGradient y2="0" x2="1" y1="0" x1="0" id="grad1">
              <stop stopColor="#5ebd3e" offset="0%"></stop>
              <stop stopColor="#ffb900" offset="33%"></stop>
              <stop stopColor="#f78200" offset="67%"></stop>
              <stop stopColor="#e23838" offset="100%"></stop>
            </linearGradient>
            <linearGradient y2="0" x2="0" y1="0" x1="1" id="grad2">
              <stop stopColor="#e23838" offset="0%"></stop>
              <stop stopColor="#973999" offset="33%"></stop>
              <stop stopColor="#009cdf" offset="67%"></stop>
              <stop stopColor="#5ebd3e" offset="100%"></stop>
            </linearGradient>
          </defs>
          <g strokeWidth="16" strokeLinecap="round" fill="none">
            <g stroke="#ddd" className={`${styles.ip__track} dark:stroke-gray-700`}>
              <path d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56"></path>
              <path d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64"></path>
            </g>
            <g strokeDasharray="180 656">
              <path
                d="M8,64s0-56,60-56,60,112,120,112,60-56,60-56"
                strokeDashoffset="0"
                stroke="url(#grad1)"
                className={styles.ip__worm1}
              ></path>
              <path
                d="M248,64s0-56-60-56-60,112-120,112S8,64,8,64"
                strokeDashoffset="358"
                stroke="url(#grad2)"
                className={styles.ip__worm2}
              ></path>
            </g>
          </g>
        </svg>
      </main>
    </div>
  );
};

export default SecondaryLoader;