"use client";

import { useEffect, useRef } from "react";

type Particle = {
  x: number;
  y: number;
  vx: number;
  vy: number;
  size: number;
};

type ParticlePreset = "light" | "medium" | "high";

type PresetConfig = {
  minParticles: number;
  maxParticles: number;
  speed: number;
  linkDistance: number;
  dotOpacity: number;
  lineOpacity: number;
};

const PRESETS: Record<ParticlePreset, PresetConfig> = {
  light: {
    minParticles: 36,
    maxParticles: 85,
    speed: 0.38,
    linkDistance: 130,
    dotOpacity: 0.68,
    lineOpacity: 0.2,
  },
  medium: {
    minParticles: 70,
    maxParticles: 130,
    speed: 0.9,
    linkDistance: 150,
    dotOpacity: 0.8,
    lineOpacity: 0.34,
  },
  high: {
    minParticles: 110,
    maxParticles: 180,
    speed: 1.35,
    linkDistance: 170,
    dotOpacity: 0.9,
    lineOpacity: 0.45,
  },
};

const presetInput = (process.env.NEXT_PUBLIC_PARTICLE_PRESET ?? "medium").toLowerCase();
const presetKey: ParticlePreset =
  presetInput === "light" || presetInput === "high" ? presetInput : "medium";
const ACTIVE_PRESET = PRESETS[presetKey];

export default function ParticlesBackground() {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }

    const ctx = canvas.getContext("2d", { alpha: true });
    if (!ctx) {
      return;
    }

    let width = 0;
    let height = 0;
    let animationId = 0;

    const particles: Particle[] = [];

    const createParticle = (): Particle => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * ACTIVE_PRESET.speed,
      vy: (Math.random() - 0.5) * ACTIVE_PRESET.speed,
      size: Math.random() * 1.8 + 0.9,
    });

    const resize = () => {
      const ratio = window.devicePixelRatio || 1;
      width = window.innerWidth;
      height = window.innerHeight;

      canvas.width = Math.floor(width * ratio);
      canvas.height = Math.floor(height * ratio);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);

      const mobileFactor = width < 768 ? 0.72 : 1;
      const targetCount = Math.floor(
        Math.min(
          ACTIVE_PRESET.maxParticles,
          Math.max(ACTIVE_PRESET.minParticles, (width * height) / 15000),
        ) * mobileFactor,
      );

      particles.length = 0;
      for (let i = 0; i < targetCount; i += 1) {
        particles.push(createParticle());
      }
    };

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      for (let i = 0; i < particles.length; i += 1) {
        const p = particles[i];

        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${ACTIVE_PRESET.dotOpacity})`;
        ctx.fill();

        for (let j = i + 1; j < particles.length; j += 1) {
          const p2 = particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const distance = Math.hypot(dx, dy);

          if (distance < ACTIVE_PRESET.linkDistance) {
            const alpha = 1 - distance / ACTIVE_PRESET.linkDistance;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = `rgba(255, 255, 255, ${alpha * ACTIVE_PRESET.lineOpacity})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }

      animationId = window.requestAnimationFrame(render);
    };

    resize();
    render();

    window.addEventListener("resize", resize);

    return () => {
      window.removeEventListener("resize", resize);
      window.cancelAnimationFrame(animationId);
    };
  }, []);

  return (
    <>
      <canvas ref={canvasRef} className="particle-canvas" aria-hidden="true" />
      <div className="particle-vignette" aria-hidden="true" />
    </>
  );
}