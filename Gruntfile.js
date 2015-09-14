module.exports = function (grunt) {
    require('time-grunt')(grunt);
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        jscs: {
            all: {
                files: {
                    src: [
                        'Gruntfile.js',
                        'slideshare/static/js/src/**/*.js'
                    ]
                }
            }
        },

        // ## //

        jshint: {
            options : {
                jshintrc: true
            },
            all: {
                files: {
                    src: [
                        'Gruntfile.js',
                        'slideshare/static/js/src/**/*.js'
                    ]
                }
            }
        },

        // ## //

        flake8: {
            all: {
                options: {
                    maxLineLength: 120,
                    hangClosing: false
                },
                src: [
                    'setup.py',
                    'slideshare/**/*.py'
                ]
            }
        }
    });

    grunt.registerTask('default', [
        'test'
    ]);

    grunt.registerTask('test', [
        'jscs:all',
        'jshint:all',
        'flake8:all'
    ]);
};
