// swithc haptic feedback

const switches = document.getElementsByClassName('t_checkbox');
for (var i = 0; i < switches.length; i++) {
    switches[i].addEventListener('click', () => {
        tg.HapticFeedback.impactOccurred('light');
    });
}