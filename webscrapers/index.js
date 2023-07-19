const PORT = 8000;

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const cheerio = require('cheerio');
const express = require('express');
const { pipeline } = require('stream'); // Import the pipeline function

const app = express();

const url = 'https://www.thenorthface.com/en-us/mens/mens-tops/mens-t-shirts-c213137';

app.get('/', async (req, res) => {
  try {
    const response = await axios.get(url);
    const html = response.data;
    const $ = cheerio.load(html);
    const imageUrls = [];

    $('.vf-picture').each((index, element) => {
      const gridItem = $(element);
      const imageSrc = gridItem.find('img').attr('src');
      imageUrls.push(imageSrc);
    });

    // Continue with further processing or return the imageUrls

    const downloadImages = imageUrls.map((imageUrl, index) => {
      const imagePath = path.join(__dirname, 'images/NorthFaceImages', `image_${index}.jpg`);
      return downloadImage(imageUrl, imagePath);
    });

    await Promise.all(downloadImages);
  } catch (error) {
    console.error('Error scraping and saving images:', error);
  }
});

async function downloadImage(imageUrl, imagePath) {
  const response = await axios.get(imageUrl, { responseType: 'stream' });

  await new Promise((resolve, reject) => {
    const fileStream = fs.createWriteStream(imagePath);
    pipeline(response.data, fileStream, (err) => {
      if (err) {
        console.error('Error saving image:', err);
        reject(err);
      } else {
        resolve();
      }
    });
  });
}

app.listen(PORT, () => console.log(`Server running on port: ${PORT}`));