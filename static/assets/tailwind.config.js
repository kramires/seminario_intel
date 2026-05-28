tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'on-tertiary-fixed': '#211b00',
        'surface-bright': '#fcf9f2',
        'background': '#fcf9f2',
        'on-secondary-container': '#4b6677',
        'inverse-on-surface': '#f3f0e9',
        'primary': '#3e5338',
        'on-secondary': '#ffffff',
        'surface-container-lowest': '#ffffff',
        'surface-container-low': '#f6f3ec',
        'on-primary-container': '#d1ebc8',
        'primary-fixed': '#d1eac7',
        'on-tertiary-fixed-variant': '#524700',
        'inverse-primary': '#b5cdac',
        'outline-variant': '#c4c8be',
        'surface-variant': '#e5e2db',
        'secondary-fixed-dim': '#aecade',
        'error-container': '#ffdad6',
        'primary-fixed-dim': '#b5cdac',
        'tertiary-container': '#beac52',
        'secondary-fixed': '#cae6fa',
        'secondary': '#476273',
        'on-error-container': '#93000a',
        'error': '#ba1a1a',
        'tertiary-fixed-dim': '#dac769',
        'on-tertiary': '#ffffff',
        'on-error': '#ffffff',
        'primary-container': '#556b4f',
        'on-tertiary-container': '#4a4000',
        'on-primary-fixed-variant': '#374c32',
        'surface-dim': '#dcdad3',
        'on-surface': '#1c1c18',
        'on-secondary-fixed-variant': '#2f4a5a',
        'inverse-surface': '#31312c',
        'on-surface-variant': '#434841',
        'tertiary-fixed': '#f7e382',
        'surface-container': '#f1eee7',
        'on-primary': '#ffffff',
        'secondary-container': '#c7e4f7',
        'on-primary-fixed': '#0c200a',
        'on-background': '#1c1c18',
        'surface': '#fcf9f2',
        'surface-container-high': '#ebe8e1',
        'tertiary': '#6c5e06',
        'surface-tint': '#4e6449',
        'outline': '#747870',
        'surface-container-highest': '#e5e2db',
        'on-secondary-fixed': '#001e2c'
      },
      borderRadius: {
        DEFAULT: '0.25rem',
        lg: '0.5rem',
        xl: '0.75rem',
        full: '9999px'
      },
      spacing: {
        'container-max': '1280px',
        'margin-mobile': '1.5rem',
        gutter: '2rem',
        'section-gap': '6rem',
        'component-gap': '1.5rem'
      },
      fontFamily: {
        'body-md': ['Hanken Grotesk'],
        'headline-xl': ['Hanken Grotesk'],
        'display-lg-mobile': ['Hanken Grotesk'],
        'label-caps': ['Inter'],
        'display-lg': ['Hanken Grotesk'],
        'headline-md': ['Hanken Grotesk'],
        'headline-xl-mobile': ['Hanken Grotesk'],
        'body-lg': ['Hanken Grotesk']
      },
      fontSize: {
        'body-md': ['16px', { lineHeight: '1.6', fontWeight: '400' }],
        'headline-xl': ['48px', { lineHeight: '1.2', fontWeight: '600' }],
        'display-lg-mobile': ['40px', { lineHeight: '1.1', fontWeight: '700' }],
        'label-caps': ['12px', { lineHeight: '1.0', letterSpacing: '0.1em', fontWeight: '600' }],
        'display-lg': ['64px', { lineHeight: '1.1', letterSpacing: '-0.02em', fontWeight: '700' }],
        'headline-md': ['32px', { lineHeight: '1.3', fontWeight: '500' }],
        'headline-xl-mobile': ['32px', { lineHeight: '1.2', fontWeight: '600' }],
        'body-lg': ['20px', { lineHeight: '1.6', fontWeight: '400' }]
      }
    }
  }
};
