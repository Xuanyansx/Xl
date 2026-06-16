/**
 * @param {...(null|boolean|number|string|Array|Object)} args
 * @return {number}
 */
var argumentsLength = function(...args) {
	console.log(args);
};

argumentsLength(1,2,3,4,5);
/**
 * argumentsLength(1, 2, 3); // 3
 */