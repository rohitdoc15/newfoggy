const twitterScraper = require('easytwitterscraper')

async function getInfoAboutTweet (url) {
  const info = await twitterScraper.getTweetByURL(url)
  return info
}

async function getInfoAboutTwitterUser (url) {
  const info = await twitterScraper.getUserByURL(url)
  return info
}

// Getting the URL from the command line arguments
const url = process.argv[2];

getInfoAboutTweet(url)
.then(info => {
  // console.log(info);
  console.log(JSON.stringify(info));
})
.catch(err => console.error(err));

