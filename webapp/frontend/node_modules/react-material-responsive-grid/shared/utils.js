'use strict';

Object.defineProperty(exports, "__esModule", {
	value: true
});
exports.pushSizeClassNames = exports.isSizeValid = exports.validSizes = exports.getClass = undefined;

var _materialResponsiveGrid = require('material-responsive-grid/material-responsive-grid.css');

var _materialResponsiveGrid2 = _interopRequireDefault(_materialResponsiveGrid);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var getClass = exports.getClass = function getClass(className) {
	return _materialResponsiveGrid2.default && _materialResponsiveGrid2.default[className] ? _materialResponsiveGrid2.default[className] : className;
};

var validSizes = exports.validSizes = ['xs4', 'xs8', 'sm8', 'sm12', 'md12', 'lg12', 'xl12', 'sm', 'md', 'lg', 'xl'];

var isSizeValid = exports.isSizeValid = function isSizeValid(size) {
	return validSizes.indexOf(size) >= 0;
};

var pushSizeClassNames = exports.pushSizeClassNames = function pushSizeClassNames(array, sizes) {
	var preClassName = arguments.length > 2 && arguments[2] !== undefined ? arguments[2] : '';
	var postClassName = arguments.length > 3 && arguments[3] !== undefined ? arguments[3] : '';

	sizes.forEach(function (size) {
		if (isSizeValid(size)) {
			array.push(getClass('' + preClassName + size + postClassName));
		}
	});
};

exports.default = {
	getClass: getClass,
	validSizes: validSizes,
	isSizeValid: isSizeValid,
	pushSizeClassNames: pushSizeClassNames
};