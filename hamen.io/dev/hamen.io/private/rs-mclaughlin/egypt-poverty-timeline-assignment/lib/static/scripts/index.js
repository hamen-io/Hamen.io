const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function diff(range) {
    return range >= 0 ? 1 : -1
};

function daysInMonth(month) {
    return new Date(2020, month, 0).getDate();
}

function ordinalSuffixFor(day) {
    if (day >= 11 && day <= 13) {
        return "th";
    }
    switch (day % 10) {
        case 1: return "st";
        case 2: return "nd";
        case 3: return "rd";
        default: return "th";
    }
}

function fadeImage(sourceImage, destImage) {
    if (sourceImage && destImage) {
        sourceImage.style.opacity = "0%";
        destImage.style.opacity = "100%";
    }
};

window.addEventListener("DOMContentLoaded", () => {
    var currentSlide = 0;

    const captionList = document.querySelector("#slide-captions");
    const paragraphList = document.querySelector("#slide-paragraphs");
    const dateList = document.querySelector("#slide-dates");
    captionList.style.width = (100 * slides.length) + "vw";
    paragraphList.style.width = (100 * slides.length) + "vw";
    dateList.style.width = (100 * slides.length) + "vw";

    slides.forEach((slide, i) => {
        const slideCaption = document.createElement("p");
        slideCaption.classList.add("caption", "slide-caption");
        slideCaption.innerText = slide.caption;
        captionList.appendChild(slideCaption);

        const slideDate = document.createElement("p");
        slideDate.classList.add("slide-date");
        slideDate.innerText = months[slide.date.month - 1] + " " + slide.date.day + ordinalSuffixFor(slide.date.day);
        dateList.appendChild(slideDate);

        const slideBody = document.createElement("div");
        const slideBodyText = document.createElement("p");
        slideBodyText.classList.add("slide-text");
        slideBodyText.innerHTML = slide.description.split("<cite>")[0];
        slideBody.appendChild(slideBodyText);
        slideBody.innerHTML += "<cite>" + (slide.description.split("<cite>")[1] || "</cite>");
        paragraphList.appendChild(slideBody);

        const backgroundImageWrapper = document.querySelector("#background-image");
        const imageElement = document.createElement("img");
        imageElement.src = slide.image;
        imageElement.style.opacity = i === 0 ? "100%" : "0%";
        imageElement.style.transition = "600ms";
        imageElement.setAttribute("index", `_${i}`);
        imageElement.setAttribute("width", "100%");
        backgroundImageWrapper.appendChild(imageElement);
    });

    var isAnimating = false;

    const toSlide = newSlide => {
        if (newSlide < 0 || newSlide >= slides.length) {
            return;
        }

        if (isAnimating) return;
        isAnimating = true;

        const backgroundImageWrapper = document.querySelector("#background-image");
        fadeImage(backgroundImageWrapper.querySelector(`[index=_${newSlide + 1}]`), backgroundImageWrapper.querySelector(`[index=_${newSlide}]`))

        // Change year:
        const yearLabel = document.querySelector("#year");
        const initialYear = parseFloat(yearLabel.innerText) || slides[currentSlide].date.year;
        const targetYear = slides[newSlide].date.year;
        const difference = targetYear - initialYear;
        const transitionTime = 500;
        let currentYear = initialYear;
        const direction = difference / Math.abs(difference); // +1 or -1
        const yearAnimation = setInterval(() => {
            yearLabel.innerText = currentYear;
            if (currentYear === targetYear) {
                return clearInterval(yearAnimation);
            }

            currentYear += direction;
        }, (transitionTime / 1.5) / Math.abs(targetYear - currentYear));

        // Translate rows
        captionList.style.transform = `translateX(${100 * ((slides.length / 2 - 0.5) - newSlide)}vw)`;
        captionList.style.transition = transitionTime + "ms";
        dateList.style.transform = `translateX(${100 * ((slides.length / 2 - 0.5) - newSlide)}vw)`;
        dateList.style.transition = transitionTime + "ms";
        paragraphList.style.transform = `translateX(${100 * ((slides.length / 2 - 0.5) - newSlide)}vw)`;
        paragraphList.style.transition = transitionTime + "ms";

        setTimeout(() => {
            isAnimating = false;
        }, transitionTime + 250);

        currentSlide = newSlide;
    };

    document.querySelector("#navigation #next-slide").addEventListener("click", () => toSlide(currentSlide + 1));
    document.querySelector("#navigation #prev-slide").addEventListener("click", () => toSlide(currentSlide - 1));
    window.addEventListener("keydown", e => {
        if (e.key === "ArrowLeft") {
            toSlide(currentSlide - 1);
        } else if (e.key === "ArrowRight") {
            toSlide(currentSlide + 1);
        }
    })

    toSlide(0);
})
