// static/js/index.js

document.addEventListener('DOMContentLoaded', function () {
    // Add hover animation to the button
    const button = document.querySelector('button');

    button.addEventListener('mouseover', function () {
        button.style.transform = 'scale(1.1)';
        button.style.transition = 'transform 0.3s ease-in-out';
    });

    button.addEventListener('mouseout', function () {
        button.style.transform = 'scale(1)';
    });
});
