module.exports = {
  content: ["./pages/*.{html,js}", "./index.html", "./js/*.js"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#E67E22", // orange-600
          50: "#FDF2E9",
          100: "#FCE4CA",
          200: "#F9C74F",
          300: "#F6A623",
          400: "#F39C12",
          500: "#E67E22",
          600: "#D35400",
          700: "#BA4A00",
          800: "#A04000",
          900: "#873600",
        },
        secondary: {
          DEFAULT: "#2C3E50", // slate-800
          50: "#F8FAFC",
          100: "#F1F5F9",
          200: "#E2E8F0",
          300: "#CBD5E1",
          400: "#94A3B8",
          500: "#64748B",
          600: "#475569",
          700: "#334155",
          800: "#2C3E50",
          900: "#1E293B",
        },
        accent: {
          DEFAULT: "#F39C12", // amber-500
          50: "#FFFBEB",
          100: "#FEF3C7",
          200: "#FDE68A",
          300: "#FCD34D",
          400: "#FBBF24",
          500: "#F39C12",
          600: "#D97706",
          700: "#B45309",
          800: "#92400E",
          900: "#78350F",
        },
        background: "#FAFBFC", // gray-50
        surface: "#FFFFFF", // white
        text: {
          primary: "#2C3E50", // slate-800
          secondary: "#7F8C8D", // gray-500
        },
        success: {
          DEFAULT: "#27AE60", // green-600
          50: "#F0FDF4",
          100: "#DCFCE7",
          200: "#BBF7D0",
          300: "#86EFAC",
          400: "#4ADE80",
          500: "#22C55E",
          600: "#27AE60",
          700: "#15803D",
          800: "#166534",
          900: "#14532D",
        },
        warning: {
          DEFAULT: "#F1C40F", // yellow-400
          50: "#FEFCE8",
          100: "#FEF9C3",
          200: "#FEF08A",
          300: "#FDE047",
          400: "#F1C40F",
          500: "#EAB308",
          600: "#CA8A04",
          700: "#A16207",
          800: "#854D0E",
          900: "#713F12",
        },
        error: {
          DEFAULT: "#E74C3C", // red-500
          50: "#FEF2F2",
          100: "#FEE2E2",
          200: "#FECACA",
          300: "#FCA5A5",
          400: "#F87171",
          500: "#E74C3C",
          600: "#DC2626",
          700: "#B91C1C",
          800: "#991B1B",
          900: "#7F1D1D",
        },
      },
      fontFamily: {
        sans: ['Open Sans', 'sans-serif'],
        heading: ['Inter', 'sans-serif'],
        caption: ['Source Sans Pro', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'fluid-xs': 'clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)',
        'fluid-sm': 'clamp(0.875rem, 0.8rem + 0.375vw, 1rem)',
        'fluid-base': 'clamp(1rem, 0.9rem + 0.5vw, 1.125rem)',
        'fluid-lg': 'clamp(1.125rem, 1rem + 0.625vw, 1.25rem)',
        'fluid-xl': 'clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem)',
        'fluid-2xl': 'clamp(1.5rem, 1.3rem + 1vw, 1.875rem)',
        'fluid-3xl': 'clamp(1.875rem, 1.6rem + 1.375vw, 2.25rem)',
      },
      boxShadow: {
        'subtle': '0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06)',
        'elevated': '0 4px 6px rgba(0, 0, 0, 0.1)',
        'floating': '0 10px 25px rgba(0, 0, 0, 0.15)',
      },
      borderRadius: {
        'lg': '8px',
        'md': '4px',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
      },
      transitionTimingFunction: {
        'ease-out': 'cubic-bezier(0, 0, 0.2, 1)',
        'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      scale: {
        '98': '0.98',
        '105': '1.05',
      },
      animation: {
        'fade-in': 'fadeIn 200ms ease-out',
        'slide-up': 'slideUp 200ms ease-out',
        'pulse-subtle': 'pulseSubtle 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        pulseSubtle: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
      },
    },
  },
  plugins: [],
}