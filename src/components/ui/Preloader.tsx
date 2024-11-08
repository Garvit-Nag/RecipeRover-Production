import React from 'react';
import styles from './Preloader.module.css';

const Preloader: React.FC = () => {
  return (
    <div className={styles.preloaderContainer}>
      <svg className={styles.pl} viewBox="0 0 128 128" width="128px" height="128px" role="img" aria-label="A pan being used to flip a blob resembling bacon as it splashes drops of grease in and out">
        <clipPath id="pan-clip">
          <rect rx="12" ry="14" x="4" y="52" width="68" height="28" />
        </clipPath>
        <defs>
          <linearGradient id="pl-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#000" />
            <stop offset="100%" stopColor="#fff" />
          </linearGradient>
          <mask id="pl-mask">
            <rect x="0" y="0" width="88" height="80" fill="url(#pl-grad)" />
          </mask>
        </defs>
        <g fill="currentColor">
          <g fill="none" strokeDasharray="20 221" strokeDashoffset="20" strokeLinecap="round" strokeWidth="4">
            <g stroke="hsl(38,90%,50%)">
              <circle className={styles.plRing} cx="44" cy="40" r="35" transform="rotate(90,44,40)" />
            </g>
            <g stroke="hsl(8,90%,40%)" mask="url(#pl-mask)">
              <circle className={styles.plRing} cx="44" cy="40" r="35" transform="rotate(90,44,40)" />
            </g>
          </g>
          <g fill="hsla(223,10%,70%,0)">
            <g className={`${styles.plDrop} ${styles.plDrop1}`}>
              <circle className={styles.plDropInner} cx="13" cy="60" r="2" />
            </g>
            <g className={`${styles.plDrop} ${styles.plDrop2}`}>
              <circle className={styles.plDropInner} cx="13" cy="60" r="2" />
            </g>
            <g className={`${styles.plDrop} ${styles.plDrop3}`}>
              <circle className={styles.plDropInner} cx="67" cy="72" r="2" />
            </g>
            <g className={`${styles.plDrop} ${styles.plDrop4}`}>
              <circle className={styles.plDropInner} cx="67" cy="72" r="2" />
            </g>
            <g className={`${styles.plDrop} ${styles.plDrop5}`}>
              <circle className={styles.plDropInner} cx="67" cy="72" r="2" />
            </g>
          </g>
          <g className={styles.plPan}>
            <rect rx="2" ry="2" x="4" y="66" width="68" height="14" clipPath="url(#pan-clip)" id="pan" />
            <rect rx="2" ry="2" x="76" y="66" width="48" height="7" />
          </g>
          <rect className={styles.plShadow} fill="hsla(223,10%,50%,0.2)" rx="3.5" ry="3.5" x="10" y="121" width="60" height="7" />
        </g>
      </svg>
    </div>
  );
};

export default Preloader;