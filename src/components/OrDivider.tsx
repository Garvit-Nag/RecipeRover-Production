import { motion } from "framer-motion";

const OrDivider = () => (
  <motion.div
    className="text-center my-8 text-white/80 flex items-center justify-center gap-4"
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.4 }}
  >
    <div className="h-px w-full bg-white/80" />
    <span className="text-lg font-medium">OR</span>
    <div className="h-px w-full bg-white/80" />
  </motion.div>
);

export default OrDivider;