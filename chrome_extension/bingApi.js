let divi = document.querySelector("#bg")


async function getPicture() {
    const response = await fetch("https://bing.biturl.top/?resolution=UHD&format=json&index=0&mkt=zh-CN")
    const data = await response.json()
    const picture = data.url
    console.log(picture)
    divi.style.backgroundImage= `url(${picture})`
}
getPicture()