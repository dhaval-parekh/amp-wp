/**
 * Internal dependencies
 */
import { elementTypes } from '../elements';
import ActionsPanel from './actions';
import ColorPanel from './color';
import BackgroundColorPanel from './backgroundColor';
import FontPanel from './font';
import RotationPanel from './rotationAngle';
import SizePanel from './size';
import PositionPanel from './position';
import TextPanel from './text';

const ACTIONS = 'actions';
const COLOR = 'color';
const FONT = 'font';
const ROTATION_ANGLE = 'rotationAngle';
const TEXT = 'text';
const SIZE = 'size';
const POSITION = 'position';
const BACKGROUND_COLOR = 'backgroundColor';

const ALL = [
	ACTIONS,
	POSITION,
	SIZE,
	BACKGROUND_COLOR,
	COLOR,
	FONT,
	TEXT,
	ROTATION_ANGLE,
];

function intersect( a, b ) {
	return a.filter( ( v ) => b.includes( v ) );
}

export function getPanels( elements ) {
	if ( elements.length === 0 ) {
		return [];
	}

	// Panels to always display, independent of the selected element.
	const sharedPanels = [
		{ type: ACTIONS, Panel: ActionsPanel },
	];
	// Find which panels all the selected elements have in common
	const selectionPanels = elements
		.map( ( { type } ) => elementTypes.find( ( elType ) => elType.type === type ).panels )
		.reduce( ( commonPanels, panels ) => intersect( commonPanels, panels ), ALL )
		.map( ( type ) => {
			switch ( type ) {
				case POSITION: return { type, Panel: PositionPanel };
				case ROTATION_ANGLE: return { type, Panel: RotationPanel };
				case SIZE: return { type, Panel: SizePanel };
				case BACKGROUND_COLOR: return { type, Panel: BackgroundColorPanel };
				case COLOR: return { type, Panel: ColorPanel };
				case FONT: return { type, Panel: FontPanel };
				case TEXT: return { type, Panel: TextPanel };
				default: throw new Error( `Unknown panel: ${ type }` );
			}
		} );
	return [
		...sharedPanels,
		...selectionPanels,
	];
}

export const PanelTypes = {
	ACTIONS,
	POSITION,
	SIZE,
	BACKGROUND_COLOR,
	COLOR,
	FONT,
	TEXT,
	ROTATION_ANGLE,
};