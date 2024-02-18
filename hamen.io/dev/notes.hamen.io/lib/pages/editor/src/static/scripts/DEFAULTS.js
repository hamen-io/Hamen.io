/**
 * A list of defaults for any configuration
 * 
 * @global
 * 
 * @type {{
 *      EDITOR: {
 *          CARET: {
 *              BLINKING_SPEED_INTERVALS: number
 *          }
 *      },
 * 
 *      PAGE: {
 *          MINIMUM_INSISTENT_WAIT: number
 *      }
 * }}
 */
const $_DEFAULTS = {
    EDITOR: {
        CARET: {
            BLINKING_SPEED_INTERVALS: 500
        }
    }, PAGE: {
        MINIMUM_INSISTENT_WAIT: 2500
    }
};