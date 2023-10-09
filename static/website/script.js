function assignPatternClass(my_element, x){
    my_element.classList.add("pattern-" + String((Number(x) - 1) % 3 + 1));
}