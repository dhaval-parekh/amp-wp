/**
 * External dependencies
 */
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 * WordPress dependencies
 */
import { __ } from '@wordpress/i18n';
import { useMemo } from '@wordpress/element';

/**
 * Internal dependencies
 */
import { useNormalizedThemesData } from '../themes-context-provider/use-normalized-themes-data';
import { IconWebsitePaintBrush } from '../svg/website-paint-brush';
import { SiteScanSourcesList } from './site-scan-sources-list';
import { SiteScanResults } from './index';

/**
 * Render a list of themes that cause AMP Incompatibility.
 *
 * @param {Object}   props           Component props.
 * @param {string}   props.className Component class name.
 * @param {string[]} props.slugs     List of theme slugs.
 */
export function ThemesWithAmpIncompatibility( { className, slugs = [], ...props } ) {
	const themesData = useNormalizedThemesData();
	const sources = useMemo( () => slugs?.map( ( slug ) => themesData?.[ slug ] ?? {
		slug,
		status: 'uninstalled',
	} ) || [], [ slugs, themesData ] );

	return (
		<SiteScanResults
			title={ __( 'Themes with AMP incompatibility', 'amp' ) }
			icon={ <IconWebsitePaintBrush /> }
			count={ slugs.length }
			sources={ sources }
			className={ classnames( 'site-scan-results--themes', className ) }
			{ ...props }
		>
			<SiteScanSourcesList
				sources={ sources }
				inactiveSourceNotice={ __( 'This theme has been deactivated since last site scan.' ) }
				uninstalledSourceNotice={ __( 'This theme has been uninstalled since last site scan.' ) }
			/>
		</SiteScanResults>
	);
}

ThemesWithAmpIncompatibility.propTypes = {
	className: PropTypes.string,
	slugs: PropTypes.arrayOf( PropTypes.string ).isRequired,
};