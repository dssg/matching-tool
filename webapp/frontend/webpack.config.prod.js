const path = require('path')

const webpack = require('webpack')
const ExtractTextPlugin = require('extract-text-webpack-plugin')

const rootAssetPath = './'

module.exports = {
  entry: ['babel-polyfill', 'whatwg-fetch', path.resolve(__dirname, './index.js')],
  output: {
    path: '../backend/static/',
    publicPath: 'http://localhost:2992/assets/',
    filename: 'output.js',
  },
  resolve: {
    root: path.resolve(__dirname, './'),
    extensions: ['', '.js']
  },
  module: {
    loaders: [
      {
        test: /\.js$/i,
        loader: 'babel-loader',
        exclude: [/node_modules/, /\.swp$/],
        query: {
          presets: ['react', 'es2015', 'stage-0']
        }
      },
      {
        test: /\.css$/i,
        loader: ExtractTextPlugin.extract('style-loader', 'css-loader')
      },
      {
        test: require.resolve("react"),
        loader: 'expose?React'
      },
      {
        test: require.resolve("react-dom"),
        loader: 'expose?ReactDOM'
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin('[name].[chunkhash].css'),
    new webpack.DefinePlugin({
      'process.env': { 'NODE_ENV': '"production"' }
    }),
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/)
  ]
}
