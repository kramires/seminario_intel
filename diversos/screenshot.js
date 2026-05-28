const puppeteer = require('puppeteer');

(async () => {
  console.log('Iniciando o Puppeteer...');
  const browser = await puppeteer.launch({ 
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  
  console.log('Navegando para o site local...');
  await page.goto('http://localhost:8501', { waitUntil: 'networkidle2', timeout: 30000 });
  
  console.log('Aguardando 5 segundos adicionais para renderização completa...');
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  console.log('Capturando screenshot...');
  await page.screenshot({ 
    path: '/Users/kramires/Desktop/seminario_inteligencia/imagens/streamlit_render.png', 
    fullPage: false 
  });
  
  console.log('Concluído!');
  await browser.close();
})();
