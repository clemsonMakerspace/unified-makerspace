
// scrapes list of majors from
// https://www.clemson.edu/degrees/index.html

e = document.querySelectorAll('[class*="ln"]')

j = []
for (let n of e) {
    a = n.querySelector('td')
    if (a) {
        j.push(a.innerHTML)
    }
}
j
