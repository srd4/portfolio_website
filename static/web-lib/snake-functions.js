require = (function () { function r(e, n, t) { function o(i, f) { if (!n[i]) { if (!e[i]) { var c = "function" == typeof require && require; if (!f && c) return c(i, !0); if (u) return u(i, !0); var a = new Error("Cannot find module '" + i + "'"); throw a.code = "MODULE_NOT_FOUND", a } var p = n[i] = { exports: {} }; e[i][0].call(p.exports, function (r) { var n = e[i][1][r]; return o(n || r) }, p, p.exports, r, e, n, t) } return n[i].exports } for (var u = "function" == typeof require && require, i = 0; i < t.length; i++)o(t[i]); return o } return r })()({
    1: [function (require, module, exports) {
        /**
         * Agrega el elemento value al comienzo de la lista. 
         * @param {*} value 
         * @param {Array} list 
         * @returns {Array}
         * @example cons(1, [2, 3]); // => [1, 2, 3]
         */
        function cons(value, list) {
            let tmp = list.slice(0);
            tmp.splice(0, 0, value);
            return tmp;
        }

        /**
         * Retorma el primer elemento de la lista
         * @param {Array} list 
         * @example first([1, 2, 3]) // => 1
         * @returns {*}
         */
        function first(list) {
            return list.slice(0, 1)[0];
        }

        /**
         * Retorna todos los elementos de la lista, excepto el primero
         * @param {Array} list 
         * @returns {Array}
         * @example rest([1, 2, 3]); // => [2, 3]
         */
        function rest(list) {
            return list.slice(1);
        }

        /**
         * La lista de entrada está vacio?
         * @param {Array} list 
         * @returns {boolean}
         * @example isEmpty([1, 2, 3]); // => false
         * @example isEmpty([]); // => true
        
         */
        function isEmpty(list) {
            if (typeof list == 'object') {
                return list.length === 0;
            }
            return false;
        }

        /**
         * Retorna verdadero si el objeto de entrada es una lista
         * @param {Array} list
         * @returns {boolean} 
         * @example isList([]); // => true
         * @example isList([1, 2]); // => true
         * @example isList(1); // => false
         * @example isList("Hola"); // => false
         */
        function isList(list) {
            return typeof list === 'object' && typeof list.length == 'number' && list.length >= 0;
        }

        /**
         * Retorna la longitud de un arreglo
         * @param {Array} list 
         * @returns {Number}
         * @example length([]); // => 0
         * @example length([2, 4]); // => 2
         */
        function length(list) {
            return list.length;
        }

        /**
         * Concatena la list2 al final de la list1. Si list2 no es un arreglo, simplemente agrega
         * este elemento al final de list1.
         * @param {Array} list1 
         * @param {Array | Object} list2 
         * @returns {Array}
         * @example append([1, 2], [3, 4]); // => [1, 2, 3, 4]
         */
        function append(list1, list2) {
            let tmp = list1.slice();
            if (typeof list2 === 'object' && list2.length >= 0) {
                tmp.push(...list2);
                return tmp;
            } else {
                tmp.push(list2);
                return tmp;
            }
        }

        /**
         * Filtra la lista l usando la función f.
         * @param {Array} l 
         * @param {function} f función booleana 
         * @returns {Array}
         * @example filter([1, 2, 3, 4, 5], x => x % 2 === 1); // => [1, 3, 5]
         */
        function filter(l, f) {
            if (isEmpty(l)) {
                return [];
            } else if (f(first(l))) {
                return cons(first(l), filter(rest(l), f));
            } else {
                return filter(rest(l), f);
            }
        }

        /**
         * Aplica la función f a cada elemento del arreglo a
         * @param {Array} a 
         * @param {function} f 
         * @returns {Array}
         * @example console.log(map([1,2,3], x => x*x)); // => [1, 4, 9]
         */
        let map = function (a, f) {
            if (isEmpty(a)) {
                return [];
            } else {
                return cons(f(first(a)), map(rest(a), f));
            }
        };

        module.exports = { cons, first, rest, isEmpty, isList, length, append, filter, map };
    }, {}], "snake-functions": [function (require, module, exports) {
        // library for basic sanke's project functions


        const { cons, first, rest, isEmpty, isList, append, length, map } = require('functional-light');

        /**
         * Creates a new object based on another object and modifying/adding given attributes.
         * @returns {object}
         * @param {object} data
         * @param attribute
         * @example make(world, { direction: "up" });
         */
        function make(data, attribute) {
            return Object.assign({}, data, attribute);
        }

        /**
         * Returns random number between 0 and canvasSize-1.
         * @returns {number}
         * @param {none}
         * @example y: random()
         */
        function random() {

            return Math.round(Math.random() * (canvasSize - 5)) + 2

        }

        /**
         * Returns list without the last element.
         * @returns {list}
         * @param {list} list
         * @example listMinOne(world.snake)
         */
        function listMinOne(list) {
            if (length(list) == 1) {
                return [];
            }
            else {
                return cons(first(list), listMinOne(rest(list)));
            }
        }

        /**
         * Returns true if a "square" object is inside list.
         * @returns {boolean}
         * @param {object} element
         * @param {list} list
         * @example inList(world.snake[0], rest(world.snake)
         */
        function inList(element, list) {
            if (isEmpty(list)) {
                return false
            }
            if (element.x == first(list).x && element.y == first(list).y) {
                return true
            }
            return inList(element, rest(list))
        }

        /**
        * Checks if head's position equals any of the body.
        * @returns {boolean}
        * @param {object} world
        * @example (ateSelf(movement(world)
        */
        function ateSelf(world) {
            if (inList(world.snake[0], rest(world.snake))) {
                return true;
            }
            return false;
        }

        /**
         * Checks if head of the snake is out of the map.
         * @returns {boolean}
         * @param {object} world
         * @example outTheMap(movement(world)
         */
        function outTheMap(world) {
            if ((world.snake[0].x >= (canvasSize - 2)) || (world.snake[0].y >= (canvasSize - 2)) || (world.snake[0].x < 2) || (world.snake[0].y < 2)) {
                return true;
            }
            return false
        }
        /**
         * if world.pause equals true, returns unchaged world.
         * @returns {boolean}
         * @param {object} world 
         * @example pause(world)
         */
        function pause(world) {
            if (world.pause == true) {
                return world
            }
        }

        /**
         * If the difficulty is medium or hard, it gives double or triple points
         * @param {object} world 
         * @returns {number}
         */
        function scoreCount(dif) {
            switch (dif) {
                case easy:
                    return 1;
                case medium:
                    return 2;
                case hard:
                    return 3;
            }
        }

        /**
         * If the position of the snake's head is equal to the position of the food the snake grows.
         * @returns {object} 
         * @param {object} world
         * @example gotFood(movement(world)
         */
        function gotFood(world) {
            if (world.snake[0].x == world.foodPos.x && world.snake[0].y == world.foodPos.y) {
                return make(world, { snake: growSnake(world), foodPos: foodSpawn(world), score: world.score + scoreCount(world.frameRate) })
            }
            return world;
        }

        /**
         * Adds one square to total length of the snake.
         * @returns {list}
         * @param {object} world
         * @example growSnake(world)
         */
        function growSnake(world) {
            len = length(world.snake)
            if (world.snake[len - 2].x > world.snake[len - 1].x) {
                return append(world.snake, { x: world.snake[len - 1].x - 1, y: world.snake[len - 1].y })
            }
            if (world.snake[len - 2].x < world.snake[len - 1].x) {
                return append(world.snake, { x: world.snake[len - 1].x + 1, y: world.snake[len - 1].y })
            }
            if (world.snake[len - 2].y < world.snake[len - 1].y) {
                return append(world.snake, { y: world.snake[len - 1].y + 1, x: world.snake[len - 1].x })
            }
            if (world.snake[len - 2].y > world.snake[len - 1].y) {
                return append(world.snake, { y: world.snake[len - 1].y - 1, x: world.snake[len - 1].x })
            }
        }

        /**
         * Moves the snake by deleting last square and adding one infront.
         * @returns {list}
         * @param {object} world
         * @example movement(world)
         */
        function movement(world) {
            switch (world.direction) {
                case "up":
                    return make(world,
                        { snake: cons(make(world.snake[0], { y: world.snake[0].y - 1 }), listMinOne(world.snake)) });
                    break;
                case "down":
                    return make(world,
                        { snake: cons(make(world.snake[0], { y: world.snake[0].y + 1 }), listMinOne(world.snake)) });
                    break;
                case "left":
                    return make(world, {
                        snake: cons(make(world.snake[0], { x: world.snake[0].x - 1 }), listMinOne(world.snake))
                    });
                    break;
                case "right":
                    return make(world, {
                        snake: cons(make(world.snake[0], { x: world.snake[0].x + 1 }), listMinOne(world.snake))
                    });
                    break;
                default:
                    return world;
            }
        }

        /**
         * Makes sure food doesn't spawn under the snake.
         * @returns {const}
         * @param {object} world
         * @example foodSpawn(world)
         */
        function foodSpawn(world) {
            const val = { x: random(), y: random() }
            if (inList(val, world.snake)) {
                return foodSpawn(world)
            }
            return val
        }


        module.exports = {
            make,
            random,
            listMinOne,
            inList,
            ateSelf,
            outTheMap,
            pause,
            gotFood,
            growSnake,
            movement,
            foodSpawn,
        };
    }, { "functional-light": 1 }]
}, {}, []);
