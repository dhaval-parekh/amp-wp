/**
 * WordPress dependencies
 */
import { useContext, useMemo, useState } from '@wordpress/element';

/**
 * External dependencies
 */
import { PREVIEW_URLS } from 'amp-settings'; // From WP inline script.

/**
 * Internal dependencies
 */
import { Options } from '../../../components/options-context-provider';
import { STANDARD } from '../../../common/constants';

export function usePreview() {
	const hasPreview = PREVIEW_URLS.length > 0;

	const { editedOptions: { theme_support: themeSupport } } = useContext( Options );
	const [ isPreviewingAMP, setIsPreviewingAMP ] = useState( themeSupport !== STANDARD );
	const [ previewedPageType, setPreviewedPageType ] = useState( hasPreview ? PREVIEW_URLS[ 0 ].type : null );

	const toggleIsPreviewingAMP = () => setIsPreviewingAMP( ( mode ) => ! mode );
	const setActivePreviewLink = ( link ) => setPreviewedPageType( link.type );

	const previewLinks = useMemo( () => PREVIEW_URLS.map( ( { url, amp_url: ampUrl, type, label } ) => ( {
		type,
		label,
		url: isPreviewingAMP ? ampUrl : url,
		isActive: type === previewedPageType,
	} ) ), [ isPreviewingAMP, previewedPageType ] );

	const previewUrl = useMemo( () => previewLinks.find( ( link ) => link.isActive )?.url, [ previewLinks ] );

	return {
		hasPreview,
		isPreviewingAMP,
		previewLinks,
		previewUrl,
		setActivePreviewLink,
		toggleIsPreviewingAMP,
	};
}
