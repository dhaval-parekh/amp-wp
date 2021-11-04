/**
 * External dependencies
 */
import PropTypes from 'prop-types';

/**
 * WordPress dependencies
 */
import { useInstanceId } from '@wordpress/compose';

const INTRINSIC_ICON_WIDTH = 59;
const INTRINSIC_ICON_HEIGHT = 44;
const INTRINSIC_STROKE_WIDTH = 2;

export function IconLandscapeHillsCogsAlt( { width = INTRINSIC_ICON_WIDTH, ...props } ) {
	const clipPathId = `clip-icon-landscape-hills-cogs-alt-${ useInstanceId( IconLandscapeHillsCogsAlt ) }`;
	const strokeWidth = INTRINSIC_STROKE_WIDTH * ( INTRINSIC_ICON_WIDTH / width );

	return (
		<svg viewBox={ `0 0 ${ INTRINSIC_ICON_WIDTH } ${ INTRINSIC_ICON_HEIGHT }` } width={ width } fill="none" xmlns="http://www.w3.org/2000/svg" { ...props }>
			<path d="M22.338 42.001s10.762-10.545 33.9-5.458" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" strokeLinecap="round" strokeLinejoin="round" />
			<path d="M29.379 37.814S15.763 30.246 3.481 34.93m44.413 4.28c-2.79-1.395-5.334-.558-5.241-.34" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" strokeLinecap="round" strokeLinejoin="round" />
			<mask id={ clipPathId } maskUnits="userSpaceOnUse" x="5.396" y="28.18" width="12" height="8" fill="#000">
				<path fill="#fff" d="M5.396 28.18h12v8h-12z" />
				<path d="M8.072 33.629c-.528-.186-.838-.869-.59-1.396.218-.527.93-.775 1.427-.496-.062-.372.186-.745.527-.869a.92.92 0 0 1 .993.28c.217-.62.9-1.024 1.582-.962.496.062.93.372 1.147.837.28-.279.806-.279 1.086.031.279.28.248.807-.062 1.086.372-.093.775.062.961.372.186.31.217.745 0 1.055" />
			</mask>
			<path d="M7.406 35.515a2 2 0 1 0 1.331-3.772l-1.331 3.772Zm.076-3.282 1.81.852.04-.09-1.85-.762Zm1.427-.496-.98 1.743a2 2 0 0 0 2.953-2.072l-1.973.329Zm1.52-.59L8.85 32.375a2 2 0 0 0 3.466-.567l-1.887-.66Zm1.582-.961.248-1.985a1.903 1.903 0 0 0-.067-.007l-.181 1.992Zm1.147.837-1.812.846a2 2 0 0 0 3.226.569l-1.414-1.415Zm1.086.031-1.487 1.338.072.077 1.415-1.415Zm-.062 1.086-1.338-1.487a2 2 0 0 0 1.823 3.427l-.485-1.94Zm-.677.28a2 2 0 1 0 3.277 2.294l-3.277-2.294Zm-4.768-.677c.34.12.512.352.585.521.076.176.13.48-.03.82l-3.62-1.703a3.004 3.004 0 0 0-.021 2.472c.298.689.888 1.356 1.755 1.662l1.331-3.772Zm.595 1.252a.997.997 0 0 1-.584.576 1 1 0 0 1-.82-.091l1.962-3.486c-.83-.467-1.743-.449-2.456-.2-.713.247-1.439.799-1.801 1.677l3.699 1.524Zm1.55-1.587a1.24 1.24 0 0 1-.165.861c-.123.198-.32.378-.597.479l-1.367-3.76c-1.147.418-2.054 1.653-1.817 3.078l3.946-.658Zm-.762 1.34c-.277.1-.518.08-.685.033a1.136 1.136 0 0 1-.585-.406l3.158-2.455c-.76-.978-2.114-1.346-3.255-.931l1.367 3.759Zm2.197-.94a.587.587 0 0 1-.24.316.399.399 0 0 1-.248.054l.363-3.984c-1.495-.136-3.099.715-3.65 2.293l3.774 1.321Zm-.555.362a.536.536 0 0 1-.416-.3l3.624-1.692a3.464 3.464 0 0 0-2.71-1.978l-.497 3.97Zm2.81.268a1.254 1.254 0 0 1-.91.38 1.256 1.256 0 0 1-.905-.426l2.973-2.676c-1.064-1.182-2.916-1.177-3.986-.107l2.828 2.829Zm-1.742.03a1.297 1.297 0 0 1-.393-.986c.015-.258.123-.574.407-.829l2.676 2.974a2.793 2.793 0 0 0 .91-1.915 2.704 2.704 0 0 0-.772-2.072l-2.829 2.829Zm1.837 1.612c-.23.058-.457.037-.656-.04a1.182 1.182 0 0 1-.583-.499l3.43-2.058c-.68-1.132-2.014-1.57-3.161-1.283l.97 3.88Zm-1.239-.539a.919.919 0 0 1-.133-.46 1.12 1.12 0 0 1 .21-.661l3.277 2.294c.767-1.097.573-2.403.076-3.23l-3.43 2.057Z" fill="#2459E7" mask={ `url(#${ clipPathId })` } />
			<path d="m3.481 19.719.652 1.83 1.83.651-1.83.651-.652 1.83-.651-1.83L1 22.2l1.83-.651.651-1.83Z" fill="#fff" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" strokeLinecap="round" strokeLinejoin="round" />
			<path d="m37.508 22.858.374 2.918 2.07.723 1.468 2.185-.419 2.13 2.864 1.512 1.576-1.587 2.614-.434 1.951 1.332 2.185-1.468-.554-2.005 1.511-2.864 2.065-.858-.434-2.614-2.07-.723-1.772-2.245.419-2.13-2.56-1.452-1.636 1.891-2.554.13-2.255-1.391-1.82 1.222.493 2.31-1.51 2.864-2.006.554Z" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" />
			<path d="M45.733 26.845a3.102 3.102 0 1 0 1.196-6.087 3.102 3.102 0 0 0-1.196 6.087ZM35.74 14.167l3.108 1.876-.718 3.652-3.587.559-.907 1.402.863 3.646-3.277 2.201-3.049-2.18-1.641.31-1.511 2.864-3.957-.778-.314-3.223-1.647-1.272-3.038.984-2.2-3.278 1.815-2.804-.31-1.641-3.108-1.875.718-3.652 3.587-.56.968-1.706-.924-3.342 3.218-1.896 3.048 2.18 1.701-.615 1.512-2.863 3.956.777.619 3.283 1.342 1.212 3.342-.924 2.26 2.973-2.12 2.745.25 1.945Z" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" />
			<path d="M24.957 18.37a3.102 3.102 0 1 0 1.197-6.086 3.102 3.102 0 0 0-1.197 6.086Z" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" />
			<path d="M24.365 21.38a6.172 6.172 0 1 0 2.38-12.112 6.172 6.172 0 0 0-2.38 12.113Z" stroke="#2459E7" strokeWidth={ strokeWidth } strokeMiterlimit="10" />
		</svg>
	);
}
IconLandscapeHillsCogsAlt.propTypes = {
	width: PropTypes.number,
};
