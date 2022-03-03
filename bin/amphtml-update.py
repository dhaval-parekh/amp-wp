"""
This script is used to generate the 'class-amp-allowed-tags-generated.php'
file that is used by the class AMP_Tag_And_Attribute_Sanitizer.

A bash script, amphtml-update.sh, is provided to automatically run this script.  To run the bash script, type:

`bash amphtml-update.sh`

from within a Linux environment such as VVV.

See the Updating Allowed Tags and Attributes section of the Engineering Guidelines
https://github.com/ampproject/amp-wp/wiki/Engineering-Guidelines#updating-allowed-tags-and-attributes.

Then have fun sanitizing your AMP posts!
"""

import glob
import logging
import os
import re
import subprocess
import sys
import tempfile
import collections
import json
import google
import imp

seen_spec_names = set()

# Note: This is a temporary measure while waiting for resolution of <https://github.com/ampproject/amphtml/issues/36749#issuecomment-996160595>.
latest_extensions_file_path = os.path.join( os.path.realpath( os.path.dirname(__file__) ), 'latest-extension-versions.json' )

def Die(msg):
	print >> sys.stderr, msg
	sys.exit(1)


def SetupOutDir(out_dir):
	"""Sets up a clean output directory.

	Args:
		out_dir: directory name of the output directory.
	"""

	if os.path.exists(out_dir):
		subprocess.check_call(['rm', '-rf', out_dir])
	os.mkdir(out_dir)


def GenValidatorPb2Py(validator_directory, out_dir):
	"""Calls the proto compiler to generate validator_pb2.py.

	Args:
		validator_directory: directory name of the validator.
		out_dir: directory name of the output directory.
	"""

	os.chdir( validator_directory )
	subprocess.check_call(['protoc', 'validator.proto', '--python_out=%s' % out_dir])
	os.chdir( out_dir )
	open('__init__.py', 'w').close()

def GenValidatorProtoascii(validator_directory, out_dir):
	"""Assembles the validator protoascii file from the main and extensions.

	Args:
		validator_directory: directory for where the validator is located, inside the amphtml repo.
		out_dir: directory name of the output directory.
	"""

	protoascii_segments = [
		open(os.path.join(validator_directory, 'validator-main.protoascii')).read(),
		open(os.path.join(validator_directory, 'validator-svg.protoascii')).read(),
		open(os.path.join(validator_directory, 'validator-css.protoascii')).read()
	]
	extensions = glob.glob(os.path.join(validator_directory, '../extensions/*/validator-*.protoascii'))
	extensions.sort()
	for extension in extensions:
		protoascii_segments.append(open(extension).read())
	f = open('%s/validator.protoascii' % out_dir, 'w')
	f.write(''.join(protoascii_segments))
	f.close()


def GeneratePHP(repo_directory, out_dir):
	"""Generates PHP for WordPress AMP plugin to consume.

	Args:
		validator_directory: directory for where the validator is located, inside the amphtml repo.
		out_dir: directory name of the output directory
	"""

	allowed_tags, attr_lists, descendant_lists, reference_points, versions = ParseRules(repo_directory, out_dir)

	expected_spec_names = (
		'style amp-custom',
		'style[amp-keyframes]',
	)
	for expected_spec_name in expected_spec_names:
		if expected_spec_name not in seen_spec_names:
			raise Exception( 'Missing spec: %s' % expected_spec_name )

	#Generate the output
	out = []
	GenerateHeaderPHP(out)
	GenerateSpecVersionPHP(out, versions)
	GenerateDescendantListsPHP(out, descendant_lists)
	GenerateAllowedTagsPHP(out, allowed_tags)
	GenerateLayoutAttributesPHP(out, attr_lists)
	GenerateGlobalAttributesPHP(out, attr_lists)
	GenerateReferencePointsPHP(out, reference_points)
	GenerateFooterPHP(out)

	# join out array into a single string and remove unneeded whitespace
	output = re.sub("\\(\\s*\\)", "()", '\n'.join(out))

	# replace 'True' with true and 'False' with false
	output = re.sub("'True'", "true", output)
	output = re.sub("'False'", "false", output)

	# Write the php file to STDOUT.
	print output

def GenerateHeaderPHP(out):
	# Output the file's header
	out.append('<?php')
	out.append('/**')
	out.append(' * Generated by %s - do not edit.' % os.path.basename(__file__))
	out.append(' *')
	out.append(' * This is a list of HTML tags and attributes that are allowed by the')
	out.append(' * AMP specification. Note that tag names have been converted to lowercase.')
	out.append(' *')
	out.append(' * Note: This file only contains tags that are relevant to the `body` of')
	out.append(' * an AMP page. To include additional elements modify the variable')
	out.append(' * `mandatory_parent_denylist` in the amp_wp_build.py script.')
	out.append(' *')
	out.append(' * phpcs:ignoreFile')
	out.append(' *')
	out.append(' * @internal')
	out.append(' */')
	out.append('class AMP_Allowed_Tags_Generated {')
	out.append('')

def GenerateSpecVersionPHP(out, versions):
	# Output the version of the spec file and matching validator version
	if versions['spec_file_revision']:
		out.append('\tprivate static $spec_file_revision = %d;' % versions['spec_file_revision'])
	if versions['min_validator_revision_required']:
		out.append('\tprivate static $minimum_validator_revision_required = %d;' % versions['min_validator_revision_required'])

def GenerateDescendantListsPHP(out, descendant_lists):
	out.append('')
	out.append('\tprivate static $descendant_tag_lists = %s;' % Phpize( descendant_lists, 1 ).lstrip() )


def GenerateAllowedTagsPHP(out, allowed_tags):
	# Output the allowed tags dictionary along with each tag's allowed attributes
	out.append('')
	out.append('\tprivate static $allowed_tags = %s;' % Phpize( allowed_tags, 1 ).lstrip() )


def GenerateLayoutAttributesPHP(out, attr_lists):
	# Output the attribute list allowed for layouts.
	out.append('')
	out.append('\tprivate static $layout_allowed_attrs = %s;' % Phpize( attr_lists['$AMP_LAYOUT_ATTRS'], 1 ).lstrip() )
	out.append('')


def GenerateGlobalAttributesPHP(out, attr_lists):
	# Output the globally allowed attribute list.
	out.append('')
	out.append('\tprivate static $globally_allowed_attrs = %s;' % Phpize( attr_lists['$GLOBAL_ATTRS'], 1 ).lstrip() )
	out.append('')

def GenerateReferencePointsPHP(out, reference_points):
	# Output the reference points.
	out.append('')
	out.append('\tprivate static $reference_points = %s;' % Phpize( reference_points, 1 ).lstrip() )
	out.append('')

def GenerateFooterPHP(out):
	# Output the footer.
	out.append('''
	/**
	 * Get allowed tags.
	 *
	 * @since 0.5
	 * @return array Allowed tags.
	 */
	public static function get_allowed_tags() {
		return self::$allowed_tags;
	}

	/**
	 * Get extension specs.
	 *
	 * @since 1.5
	 * @internal
	 * @return array Extension specs, keyed by extension name.
	 */
	public static function get_extension_specs() {
		static $extension_specs = [];

		if ( ! empty( $extension_specs ) ) {
			return $extension_specs;
		}

		foreach ( self::get_allowed_tag( 'script' ) as $script_spec ) {
			if ( isset( $script_spec[ AMP_Rule_Spec::TAG_SPEC ]['extension_spec'] ) ) {
				$extension_specs[ $script_spec[ AMP_Rule_Spec::TAG_SPEC ]['extension_spec']['name'] ] = $script_spec[ AMP_Rule_Spec::TAG_SPEC ]['extension_spec'];
			}
		}

		return $extension_specs;
	}

	/**
	 * Get allowed tag.
	 *
	 * Get the rules for a single tag so that the entire data structure needn't be passed around.
	 *
	 * @since 0.7
	 * @param string $node_name Tag name.
	 * @return array|null Allowed tag, or null if the tag does not exist.
	 */
	public static function get_allowed_tag( $node_name ) {
		if ( isset( self::$allowed_tags[ $node_name ] ) ) {
			return self::$allowed_tags[ $node_name ];
		}
		return null;
	}

	/**
	 * Get descendant tag lists.
	 *
	 * @since 1.1
	 * @return array Descendant tags list.
	 */
	public static function get_descendant_tag_lists() {
		return self::$descendant_tag_lists;
	}

	/**
	 * Get allowed descendant tag list for a tag.
	 *
	 * Get the descendant rules for a single tag so that the entire data structure needn't be passed around.
	 *
	 * @since 1.1
	 * @param string $name Name for the descendants list.
	 * @return array|bool Allowed tags list, or false if there are no restrictions.
	 */
	public static function get_descendant_tag_list( $name ) {
		if ( isset( self::$descendant_tag_lists[ $name ] ) ) {
			return self::$descendant_tag_lists[ $name ];
		}
		return false;
	}

	/**
	 * Get reference point spec.
	 *
	 * @since 1.0
	 * @param string $tag_spec_name Tag spec name.
	 * @return array|null Reference point spec, or null if does not exist.
	 */
	public static function get_reference_point_spec( $tag_spec_name ) {
		if ( isset( self::$reference_points[ $tag_spec_name ] ) ) {
			return self::$reference_points[ $tag_spec_name ];
		}
		return null;
	}

	/**
	 * Get list of globally-allowed attributes.
	 *
	 * @since 0.5
	 * @return array Allowed tag.
	 */
	public static function get_allowed_attributes() {
		return self::$globally_allowed_attrs;
	}

	/**
	 * Get layout attributes.
	 *
	 * @since 0.5
	 * @return array Allowed tag.
	 */
	public static function get_layout_attributes() {
		return self::$layout_allowed_attrs;
	}''')

	out.append('')

	out.append('}')
	out.append('')


def ParseRules(repo_directory, out_dir):
	# These imports happen late, within this method because they don't necessarily
	# exist when the module starts running, and the ones that probably do
	# are checked by CheckPrereqs.

	from google.protobuf import text_format
	validator_pb2 = imp.load_source('validator_pb2', os.path.join( out_dir, 'validator_pb2.py' ))

	allowed_tags = {}
	attr_lists = {}
	descendant_lists = {}
	reference_points = {}
	versions = {}

	specfile='%s/validator.protoascii' % out_dir

	# Merge specfile with message buffers.
	rules = validator_pb2.ValidatorRules()
	text_format.Merge(open(specfile).read(), rules)

	# Record the version of this specfile and the corresponding validator version.
	if rules.HasField('spec_file_revision'):
		versions['spec_file_revision'] = rules.spec_file_revision

	if rules.HasField('min_validator_revision_required'):
		versions['min_validator_revision_required'] = rules.min_validator_revision_required

	# Build a dictionary of the named attribute lists that are used by multiple tags.
	for (field_desc, field_val) in rules.ListFields():
		if 'attr_lists' == field_desc.name:
			for attr_spec in field_val:
				attr_lists[UnicodeEscape(attr_spec.name)] = GetAttrs(attr_spec.attrs)

	# Build a dictionary of allowed tags and an associated list of their allowed
	# attributes, values and other criteria.

	# Don't include tags that have a mandatory parent with one of these tag names
	# since we're only concerned with using this tag list to validate the HTML
	# of the DOM
	mandatory_parent_denylist = [
		'$ROOT',
		'!DOCTYPE',
	]

	for (field_desc, field_val) in rules.ListFields():
		if 'tags' == field_desc.name:
			for tag_spec in field_val:

				# Ignore tags that are outside of the body
				if tag_spec.HasField('mandatory_parent') and tag_spec.mandatory_parent in mandatory_parent_denylist and tag_spec.tag_name != 'HTML':
					continue

				# Ignore deprecated tags (except for amp-sidebar in amp-story for now).
				if tag_spec.HasField('deprecation') and 'AMP-SIDEBAR' != tag_spec.tag_name:
					continue

				# Handle the special $REFERENCE_POINT tag
				if '$REFERENCE_POINT' == tag_spec.tag_name:
					gotten_tag_spec = GetTagSpec(tag_spec, attr_lists)
					if gotten_tag_spec is not None:
						reference_points[ tag_spec.spec_name ] = gotten_tag_spec
					continue

				# If we made it here, then start adding the tag_spec
				if tag_spec.tag_name.lower() not in allowed_tags:
					tag_list = []
				else:
					tag_list = allowed_tags[UnicodeEscape(tag_spec.tag_name).lower()]

				gotten_tag_spec = GetTagSpec(tag_spec, attr_lists)
				if gotten_tag_spec is not None:
					tag_list.append(gotten_tag_spec)
					allowed_tags[UnicodeEscape(tag_spec.tag_name).lower()] = tag_list
		elif 'descendant_tag_list' == field_desc.name:
			for _list in field_val:
				descendant_lists[_list.name] = []
				for val in _list.tag:

					# Skip tags specific to transformed AMP.
					if 'I-AMPHTML-SIZER' == val:
						continue

					# The img tag is currently exclusively to transformed AMP, except as descendant of amp-story-player.
					if 'IMG' == val and 'amp-story-player-allowed-descendants' != _list.name:
						continue

					descendant_lists[_list.name].append( val.lower() )

	# Separate extension scripts from non-extension scripts and gather the versions
	extension_scripts = collections.defaultdict(list)
	extension_specs_by_satisfies = dict()
	script_tags = []
	for script_tag in allowed_tags['script']:
		if 'extension_spec' in script_tag['tag_spec']:
			extension = script_tag['tag_spec']['extension_spec']['name']
			extension_scripts[extension].append(script_tag)
			if 'satisfies' in script_tag['tag_spec']:
				satisfies = script_tag['tag_spec']['satisfies']
			else:
				satisfies = extension
			if satisfies in extension_specs_by_satisfies:
				raise Exception( 'Duplicate extension script that satisfies %s.' % satisfies )

			extension_specs_by_satisfies[satisfies] = script_tag['tag_spec']['extension_spec']

			# These component lack an explicit requirement on a specific extension script:
			# - amp-selector
			# - amp-accordion
			# - amp-soundcloud
			# - amp-brightcove
			# - amp-video
			# - amp-video-iframe
			# - amp-vimeo
			# - amp-twitter
			# - amp-instagram
			# - amp-lightbox
			# - amp-facebook
			# - amp-youtube
			# - amp-social-share
			# - amp-fit-text
			# So use the one with the latest version as a fallback.
			if 'latest' in script_tag['tag_spec']['extension_spec']['version']:
				extension_specs_by_satisfies[extension] = script_tag['tag_spec']['extension_spec']
		else:
			script_tags.append(script_tag)

	# Amend the allowed_tags to supply the required versions for each component.
	for tag_name, tags in allowed_tags.items():
		for tag in tags:
			tag['tag_spec'].pop('satisfies', None) # We don't need it anymore.
			requires = tag['tag_spec'].pop('requires', [])

			if 'requires_extension' not in tag['tag_spec']:
				continue

			requires_extension_versions = {}
			for required_extension in tag['tag_spec']['requires_extension']:
				required_versions = []
				for require in requires:
					if require in extension_specs_by_satisfies:
						if required_extension != extension_specs_by_satisfies[require]['name']:
							raise Exception('Expected satisfied to be for the %s extension' % required_extension)
						required_versions = extension_specs_by_satisfies[require]['version']
						break
				if len( required_versions ) == 0:
					if required_extension in extension_specs_by_satisfies:
						if required_extension != extension_specs_by_satisfies[required_extension]['name']:
							raise Exception('Expected satisfied to be for the %s extension' % required_extension)
						required_versions = extension_specs_by_satisfies[required_extension]['version']

				if len( required_versions ) == 0:
					raise Exception('Unable to obtain any versions for %s' % required_extension)

				requires_extension_versions[required_extension] = filter( lambda ver: ver != 'latest', required_versions )
			tag['tag_spec']['requires_extension'] = requires_extension_versions

	extensions = json.load( open( os.path.join( repo_directory, 'build-system/compile/bundles.config.extensions.json' ) ) )
	latest_versions = json.load( open( latest_extensions_file_path ) )
	extensions_versions = dict()
	for extension in extensions:
		if '-impl' in extension['name'] or '-polyfill' in extension['name']:
			continue

		if extension['name'] not in extensions_versions:
			extensions_versions[ extension['name'] ] = {
				'versions': [],
				'latest': None,
			}

		if type(extension['version']) == list:
			extensions_versions[ extension['name'] ]['versions'].extend( extension['version'] )
		else:
			extensions_versions[ extension['name'] ]['versions'].append( extension['version'] )
		if extension['name'] not in latest_versions:
			raise Exception( 'There is a latest version for ' + extension['name'] )
		extensions_versions[ extension['name'] ]['latest'] = latest_versions[ extension['name'] ]

		if 'options' in extension and ( ( 'bento' in extension['options'] and extension['options']['bento'] ) or ( 'wrapper' in extension['options'] and extension['options']['wrapper'] == 'bento' ) ):
			extensions_versions[ extension['name'] ]['bento'] = {
				'version': extension['version'],
				'has_css': extension['options'].get( 'hasCss', False ),
			}

	# Merge extension scripts (e.g. Bento and non-Bento) into one script per extension.
	for extension_name in sorted(extension_scripts):
		if extension_name not in extensions_versions:
			raise Exception( 'There is a script for an unknown extension: ' + extension_name );

		extension_script_list = extension_scripts[extension_name]
		validator_versions = set(extension_script_list[0]['tag_spec']['extension_spec']['version'])
		for extension_script in extension_script_list[1:]:
			validator_versions.update(extension_script['tag_spec']['extension_spec']['version'])
		if 'latest' in validator_versions:
			validator_versions.remove('latest')

		bundle_versions = set( extensions_versions[extension_name]['versions'] )
		if not validator_versions.issubset( bundle_versions ):
			logging.info( 'Validator versions are not a subset of bundle versions: ' + extension_name )

		if 'bento' in extensions_versions[extension_name] and extensions_versions[extension_name]['bento']['version'] not in validator_versions:
			logging.info( 'Skipping bento for ' + extension_name + ' since version ' + extensions_versions[extension_name]['bento']['version'] + ' is not yet valid' )
			del extensions_versions[extension_name]['bento']

		# Verify bento_supported_version matches the version info in the bundle file.
		if 'bento_supported_version' in extension_script_list[0]['tag_spec']['extension_spec']:
			if 'bento' not in extensions_versions[extension_name]:
				logging.info( 'Warning: bento_supported_version found but bento not meta not obtained for ' + extension_name )
			elif extension_script_list[0]['tag_spec']['extension_spec']['bento_supported_version'][0] != extensions_versions[extension_name]['bento']['version']:
				logging.info( 'Warning: bento_supported_version does not match the bento meta version for ' + extension_name )

			# Remove redundant information.
			del extension_script_list[0]['tag_spec']['extension_spec']['bento_supported_version']

		validator_versions = sorted( validator_versions, key=lambda version: map(int, version.split('.') ) )
		extension_script_list[0]['tag_spec']['extension_spec']['version'] = validator_versions

		if 'bento' in extensions_versions[extension_name] and extensions_versions[extension_name]['bento']['version'] in validator_versions:
			extension_script_list[0]['tag_spec']['extension_spec']['bento'] = extensions_versions[extension_name]['bento']

		extension_script_list[0]['tag_spec']['extension_spec']['latest'] = extensions_versions[extension_name]['latest']

		extension_script_list[0]['tag_spec']['extension_spec'].pop('version_name', None)

		# Remove the spec name since we've potentially merged multiple scripts, thus it does not refer to one.
		extension_script_list[0]['tag_spec'].pop('spec_name', None)

		script_tags.append(extension_script_list[0])

	allowed_tags['script'] = script_tags

	# Now that Bento information is in hand, re-decorate specs with require_extension to indicate which
	for tag_name, tags in allowed_tags.items():
		tags_bento_status = []
		for tag in tags:
			if 'requires_extension' not in tag['tag_spec']:
				continue

			# Determine the Bento availability of all the required extensions.
			tag_extensions_with_bento = {}
			for extension, extension_versions in tag['tag_spec']['requires_extension'].items():
				if extension in extensions_versions and 'bento' in extensions_versions[extension] and extensions_versions[extension]['bento']['version'] in extension_versions:
					tag_extensions_with_bento[ extension ] = True
				else:
					tag_extensions_with_bento[ extension ] = False

			# Mark that this tag is for Bento since all its required extensions have Bento available.
			if len( tag_extensions_with_bento ) > 0 and False not in tag_extensions_with_bento.values():
				tags_bento_status.append( True )
				tag['tag_spec']['bento'] = True
			else:
				tags_bento_status.append( False )

		# Now that the ones with Bento have been identified, add flags to tag specs when there are different versions specifically for Bento:
		for tag in tags:
			if 'requires_extension' not in tag['tag_spec']:
				continue

			if False not in tags_bento_status:
				# Clear the Bento flag if _all_ of the components are for Bento.
				tag['tag_spec'].pop( 'bento', None )
			elif True in tags_bento_status and 'bento' not in tag['tag_spec']:
				# Otherwise, if _some_ of the components were exclusively for Bento, flag the others as being _not_ for Bento specifically.
				tag['tag_spec']['bento'] = False

			# Now convert requires_versions back into a list of extensions rather than an extension/versions mapping.
			tag['tag_spec']['requires_extension'] = sorted( tag['tag_spec']['requires_extension'].keys() )

	return allowed_tags, attr_lists, descendant_lists, reference_points, versions


def GetTagSpec(tag_spec, attr_lists):
	tag_dict = GetTagRules(tag_spec)
	if tag_dict is None:
		return None
	attr_dict = {}

	# First add attributes from any attribute lists to this tag.
	for (tag_field_desc, tag_field_val) in tag_spec.ListFields():
		if 'attr_lists' == tag_field_desc.name:
			for attr_list in tag_field_val:
				attr_dict.update(attr_lists[UnicodeEscape(attr_list)])

	# Then merge the spec-specific attributes on top to override any list definitions.
	attr_dict.update(GetAttrs(tag_spec.attrs))

	tag_spec_dict = {'tag_spec':tag_dict, 'attr_spec_list':attr_dict}
	if tag_spec.HasField('cdata'):
		cdata_dict = {}
		for (field_descriptor, field_value) in tag_spec.cdata.ListFields():
			if isinstance(field_value, (unicode, str, bool, int)):
				cdata_dict[ field_descriptor.name ] = field_value
			elif isinstance( field_value, google.protobuf.pyext._message.RepeatedCompositeContainer ):
				cdata_dict[ field_descriptor.name ] = []
				for value in field_value:
					entry = {}
					for (key,val) in value.ListFields():
						entry[ key.name ] = val
					cdata_dict[ field_descriptor.name ].append( entry )
			elif hasattr( field_value, '_values' ):
				cdata_dict[ field_descriptor.name ] = {}
				for _value in field_value._values:
					for (key,val) in _value.ListFields():
						cdata_dict[ field_descriptor.name ][ key.name ] = val
			elif 'css_spec' == field_descriptor.name:
				css_spec = {}

				css_spec['allowed_at_rules'] = []
				for at_rule_spec in field_value.at_rule_spec:
					if '$DEFAULT' == at_rule_spec.name:
						continue
					css_spec['allowed_at_rules'].append( at_rule_spec.name )

				for css_spec_field_name in ( 'allowed_declarations', 'declaration', 'font_url_spec', 'image_url_spec', 'validate_keyframes' ):
					if not hasattr( field_value, css_spec_field_name ):
						continue
					css_spec_field_value = getattr( field_value, css_spec_field_name )
					if isinstance(css_spec_field_value, (list, collections.Sequence, google.protobuf.internal.containers.RepeatedScalarFieldContainer, google.protobuf.pyext._message.RepeatedScalarContainer)):
						css_spec[ css_spec_field_name ] = [ val for val in css_spec_field_value ]
					elif hasattr( css_spec_field_value, 'ListFields' ):
						css_spec[ css_spec_field_name ] = {}
						for (css_spec_field_item_descriptor, css_spec_field_item_value) in getattr( field_value, css_spec_field_name ).ListFields():
							if isinstance(css_spec_field_item_value, (list, collections.Sequence, google.protobuf.internal.containers.RepeatedScalarFieldContainer, google.protobuf.pyext._message.RepeatedScalarContainer)):
								css_spec[ css_spec_field_name ][ css_spec_field_item_descriptor.name ] = [ val for val in css_spec_field_item_value ]
							else:
								css_spec[ css_spec_field_name ][ css_spec_field_item_descriptor.name ] = css_spec_field_item_value
					else:
						css_spec[ css_spec_field_name ] = css_spec_field_value

				cdata_dict['css_spec'] = css_spec
		if len( cdata_dict ) > 0:
			if 'disallowed_cdata_regex' in cdata_dict:
				for entry in cdata_dict['disallowed_cdata_regex']:
					if 'error_message' not in entry:
						raise Exception( 'Missing error_message for disallowed_cdata_regex.' );
					if entry['error_message'] not in ( 'contents', 'html comments', 'CSS i-amphtml- name prefix' ):
						raise Exception( 'Unexpected error_message "%s" for disallowed_cdata_regex.' % entry['error_message'] );
					entry['regex'] = EscapeRegex( entry['regex'] )
			tag_spec_dict['cdata'] = cdata_dict

	if 'spec_name' not in tag_spec_dict['tag_spec']:
		if 'extension_spec' in tag_spec_dict['tag_spec']:
			# CUSTOM_ELEMENT=1 (default), CUSTOM_TEMPLATE=2
			extension_type = tag_spec_dict['tag_spec']['extension_spec'].get('extension_type', 1)
			spec_name = 'script [%s=%s]' % ( 'custom-element' if 1 == extension_type else 'custom-template', tag_spec_dict['tag_spec']['extension_spec']['name'].lower() )
		else:
			spec_name = tag_spec.tag_name.lower()
	else:
		spec_name = tag_spec_dict['tag_spec']['spec_name']

	seen_spec_names.add( spec_name )

	return tag_spec_dict


def GetTagRules(tag_spec):
	tag_rules = {}

	if hasattr(tag_spec, 'also_requires_tag') and tag_spec.also_requires_tag:
		also_requires_tag_list = []
		for also_requires_tag in tag_spec.also_requires_tag:
			also_requires_tag_list.append(UnicodeEscape(also_requires_tag))
		tag_rules['also_requires_tag'] = also_requires_tag_list

	requires_extension_list = set()
	if hasattr(tag_spec, 'requires_extension') and len( tag_spec.requires_extension ) != 0:
		for requires_extension in tag_spec.requires_extension:
			requires_extension_list.add(requires_extension)

	if hasattr(tag_spec, 'requires') and len( tag_spec.requires ) != 0:
		tag_rules['requires'] = [ requires for requires in tag_spec.requires ]

	if hasattr(tag_spec, 'also_requires_tag_warning') and len( tag_spec.also_requires_tag_warning ) != 0:
		for also_requires_tag_warning in tag_spec.also_requires_tag_warning:
			matches = re.search( r'(amp-\S+) extension( \.js)? script', also_requires_tag_warning )
			if not matches:
				raise Exception( 'Unexpected also_requires_tag_warning format: ' + also_requires_tag_warning )
			requires_extension_list.add(matches.group(1))

	if len( requires_extension_list ) > 0:
		tag_rules['requires_extension'] = list( requires_extension_list )

	if hasattr(tag_spec, 'reference_points') and len( tag_spec.reference_points ) != 0:
		tag_reference_points = {}
		for reference_point_spec in tag_spec.reference_points:
			tag_reference_points[ reference_point_spec.tag_spec_name ] = {
				"mandatory": reference_point_spec.mandatory,
				"unique": reference_point_spec.unique
			}
		if len( tag_reference_points ) > 0:
			tag_rules['reference_points'] = tag_reference_points

	if tag_spec.disallowed_ancestor:
		disallowed_ancestor_list = []
		for disallowed_ancestor in tag_spec.disallowed_ancestor:
			disallowed_ancestor_list.append(UnicodeEscape(disallowed_ancestor).lower())
		tag_rules['disallowed_ancestor'] = disallowed_ancestor_list

	if tag_spec.html_format:
		has_amp_format = False
		for html_format in tag_spec.html_format:
			if 1 == html_format:
				has_amp_format = True
		if not has_amp_format:
			return None

	# Ignore transformed AMP for now.
	if tag_spec.enabled_by and 'transformed' in tag_spec.enabled_by:
		return None

	# Ignore amp-custom-length-check because the AMP plugin will indicate how close they are to the limit.
	# TODO: Remove the AMP4EMAIL check once this change is released: <https://github.com/ampproject/amphtml/pull/25246>.
	if tag_spec.HasField('spec_name') and ( str(tag_spec.spec_name) == 'style amp-custom-length-check' or 'AMP4EMAIL' in str(tag_spec.spec_name) ):
		return None

	if tag_spec.HasField('extension_spec'):
		# See https://github.com/ampproject/amphtml/blob/e37f50d/validator/validator.proto#L430-L454
		ERROR = 1
		NONE = 3
		extension_spec = {
			'requires_usage': 1 # (ERROR=1)
		}
		for field in tag_spec.extension_spec.ListFields():
			if isinstance(field[1], (list, google.protobuf.internal.containers.RepeatedScalarFieldContainer, google.protobuf.pyext._message.RepeatedScalarContainer)):
				extension_spec[ field[0].name ] = []
				for val in field[1]:
					extension_spec[ field[0].name ].append( val )
			else:
				extension_spec[ field[0].name ] = field[1]

		# Normalize ERROR and GRANDFATHERED as true, since we control which scripts are added (or removed) from the output.
		extension_spec['requires_usage'] = ( extension_spec['requires_usage'] != 3 ) # NONE=3

		if 'version' not in extension_spec:
			raise Exception( 'Missing required version field' )
		if 'name' not in extension_spec:
			raise Exception( 'Missing required name field' )

		# Unused since amp_filter_script_loader_tag() and \AMP_Tag_And_Attribute_Sanitizer::get_rule_spec_list_to_validate() just hard-codes the check for amp-mustache.
		if 'extension_type' in extension_spec:
			del extension_spec['extension_type']

		if 'deprecated_version' in extension_spec:
			del extension_spec['deprecated_version']

		if 'deprecated_allow_duplicates' in extension_spec:
			del extension_spec['deprecated_allow_duplicates']

		tag_rules['extension_spec'] = extension_spec

	if tag_spec.HasField('mandatory'):
		tag_rules['mandatory'] = tag_spec.mandatory

	if tag_spec.HasField('mandatory_alternatives'):
		tag_rules['mandatory_alternatives'] = UnicodeEscape(tag_spec.mandatory_alternatives)

	if tag_spec.HasField('mandatory_ancestor'):
		tag_rules['mandatory_ancestor'] = UnicodeEscape(tag_spec.mandatory_ancestor).lower()

	if tag_spec.HasField('mandatory_ancestor_suggested_alternative'):
		tag_rules['mandatory_ancestor_suggested_alternative'] = UnicodeEscape(tag_spec.mandatory_ancestor_suggested_alternative).lower()

	if tag_spec.HasField('mandatory_parent'):
		tag_rules['mandatory_parent'] = UnicodeEscape(tag_spec.mandatory_parent).lower()

	if tag_spec.HasField('spec_name'):
		tag_rules['spec_name'] = UnicodeEscape(tag_spec.spec_name)

	if hasattr(tag_spec, 'satisfies') and len( tag_spec.satisfies ) > 0:
		if len( tag_spec.satisfies ) > 1:
			raise Exception('More than expected was satisfied')
		tag_rules['satisfies'] = tag_spec.satisfies[0]

	if tag_spec.HasField('spec_url'):
		tag_rules['spec_url'] = UnicodeEscape(tag_spec.spec_url)

	if tag_spec.HasField('unique'):
		tag_rules['unique'] = tag_spec.unique

	if tag_spec.HasField('unique_warning'):
		tag_rules['unique_warning'] = tag_spec.unique_warning

	if tag_spec.HasField('child_tags'):
		child_tags = collections.defaultdict( lambda: [] )
		for field in tag_spec.child_tags.ListFields():
			if isinstance(field[1], (int)):
				child_tags[ field[0].name ] = field[1]
			elif isinstance(field[1], (list, google.protobuf.internal.containers.RepeatedScalarFieldContainer, google.protobuf.pyext._message.RepeatedScalarContainer)):
				for val in field[1]:
					child_tags[ field[0].name ].append( val.lower() )
		tag_rules['child_tags'] = child_tags

	if tag_spec.HasField('descendant_tag_list'):
		tag_rules['descendant_tag_list'] = tag_spec.descendant_tag_list

	if tag_spec.HasField('amp_layout'):
		amp_layout = {}
		for field in tag_spec.amp_layout.ListFields():
			if 'supported_layouts' == field[0].name:
				amp_layout['supported_layouts'] = [ val for val in field[1] ]
			else:
				amp_layout[ field[0].name ] = field[1]
		tag_rules['amp_layout'] = amp_layout

	for mandatory_of_constraint in ['mandatory_anyof', 'mandatory_oneof']:
		mandatory_of_spec = GetMandatoryOf(tag_spec.attrs, mandatory_of_constraint)
		if mandatory_of_spec:
			tag_rules[ mandatory_of_constraint ] = mandatory_of_spec

	return tag_rules


def GetAttrs(attrs):
	attr_dict = {}
	for attr_spec in attrs:

		value_dict = GetValues(attr_spec)

		if value_dict is not None:

			# Skip rules for dev mode attributes since the AMP plugin will allow them to pass through.
			# See <https://github.com/ampproject/amphtml/pull/27174#issuecomment-601391161> for how the rules are
			# defined in a way that they can never be satisfied, and thus to make the attribute never allowed.
			# This runs contrary to the needs of the AMP plugin, as the internal sanitizers are built to ignore them.
			if 'data-ampdevmode' == attr_spec.name:
				continue

			# Normalize bracketed amp-bind attribute syntax to data-amp-bind-* syntax.
			name = attr_spec.name
			if name[0] == '[':
				name = 'data-amp-bind-' + name.strip( '[]' )

			# Add attribute name and alternative_names
			attr_dict[UnicodeEscape(name)] = value_dict

	return attr_dict


def GetValues(attr_spec):
	value_dict = {}

	# Ignore transformed AMP for now.
	if 'transformed' in attr_spec.enabled_by:
		return None

	# Add alternative names
	if attr_spec.alternative_names:
		alt_names_list = []
		for alternative_name in attr_spec.alternative_names:
			alt_names_list.append(UnicodeEscape(alternative_name))
		value_dict['alternative_names'] = alt_names_list

	# Add disallowed value regex
	if attr_spec.HasField('disallowed_value_regex'):
		value_dict['disallowed_value_regex'] = EscapeRegex( attr_spec.disallowed_value_regex )

	# dispatch_key is an int
	if attr_spec.HasField('dispatch_key'):
		value_dict['dispatch_key'] = attr_spec.dispatch_key

	# mandatory is a boolean
	if attr_spec.HasField('mandatory'):
		value_dict['mandatory'] = attr_spec.mandatory

	# Add allowed value
	if attr_spec.value:
		value_dict['value'] = list( attr_spec.value )

	# value_casei
	if attr_spec.value_casei:
		value_dict['value_casei'] = list( attr_spec.value_casei )

	# value_regex
	if attr_spec.HasField('value_regex'):
		value_dict['value_regex'] = EscapeRegex( attr_spec.value_regex )

	# value_regex_casei
	if attr_spec.HasField('value_regex_casei'):
		value_dict['value_regex_casei'] = EscapeRegex( attr_spec.value_regex_casei )

	#value_properties is a dictionary of dictionaries
	if attr_spec.HasField('value_properties'):
		value_properties_dict = {}
		for (value_properties_key, value_properties_val) in attr_spec.value_properties.ListFields():
			for value_property in value_properties_val:
				property_dict = {}
				# print 'value_property.name: %s' % value_property.name
				for (key,val) in value_property.ListFields():
					if val != value_property.name:
						if isinstance(val, unicode):
							val = UnicodeEscape(val)
						property_dict[UnicodeEscape(key.name)] = val
				value_properties_dict[UnicodeEscape(value_property.name)] = property_dict
		value_dict['value_properties'] = value_properties_dict

	# value_url is a dictionary
	if attr_spec.HasField('value_url'):
		value_url_dict = {}
		for (value_url_key, value_url_val) in attr_spec.value_url.ListFields():
			if isinstance(value_url_val, (list, collections.Sequence, google.protobuf.internal.containers.RepeatedScalarFieldContainer, google.protobuf.pyext._message.RepeatedScalarContainer)):
				value_url_val_val = []
				for val in value_url_val:
					value_url_val_val.append(UnicodeEscape(val))
			else:
				value_url_val_val = value_url_val
			value_url_dict[value_url_key.name] = value_url_val_val
		value_dict['value_url'] = value_url_dict

	if hasattr(attr_spec, 'requires_extension') and len( attr_spec.requires_extension ) != 0:
		requires_extension_list = []
		for requires_extension in attr_spec.requires_extension:
			requires_extension_list.append(requires_extension)
		value_dict['requires_extension'] = requires_extension_list

	return value_dict


def UnicodeEscape(string):
	"""Helper function which escapes unicode characters.

	Args:
		string: A string which may contain unicode characters.
	Returns:
		An escaped string.
	"""
	return ('' + string).encode('unicode-escape')

def EscapeRegex(string):
	return re.sub( r'(?<!\\)/', r'\\/', string )

def GetMandatoryOf( attr, constraint ):
	"""Gets the attributes with the passed mandatory_*of constraint, if there are any.

	Args:
		attr: The attributes in which to look for the mandatory_*of constraint.
		constraint: A string of the mandatory_*of constraint, like 'mandatory_anyof'.
	Returns:
		A list of attributes that have that constraint name.
	"""
	attributes = set()
	for attr_spec in attr:
		if attr_spec.HasField(constraint):
			attributes.add(
				# Convert something like [src] to data-amp-bind-src.
				re.sub(
					"^\[(\S+)\]$",
					r"data-amp-bind-\1",
					attr_spec.name
				)
			)

	return sorted(attributes)

def Phpize(data, indent=0):
	"""Helper function to convert JSON-serializable data into PHP literals.

	Args:
		data: Any JSON-serializable.
	Returns:
		String formatted as PHP literal.
	"""
	json_string = json.dumps(data, sort_keys=True, ensure_ascii=False)

	pipe = subprocess.Popen(['php', '-r', 'var_export( json_decode( file_get_contents( "php://stdin" ), true ) );'], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
	php_stdout = pipe.communicate(input=json_string)[0]
	php_exported = php_stdout.decode()

	# Clean up formatting.
	# TODO: Just use PHPCBF for this.
	php_exported = re.sub( r'^ +', lambda match: int( round(len(match.group(0))/2) ) * '\t', php_exported, flags=re.MULTILINE )
	php_exported = php_exported.replace( 'array (', 'array(' )
	php_exported = re.sub( r' => \n\s+', ' => ', php_exported, flags=re.MULTILINE )
	php_exported = re.sub( r'^(\s+)\d+ =>\s*', r'\1', php_exported, flags=re.MULTILINE )

	# Add additional indents.
	if indent > 0:
		php_exported = re.sub( r'^', '\t' * indent, php_exported, flags=re.MULTILINE )
	return php_exported

def Main( repo_directory, out_dir ):
	"""The main method, which executes all build steps and runs the tests."""
	logging.basicConfig(format='[[%(filename)s %(funcName)s]] - %(message)s', level=logging.INFO)

	validator_directory = os.path.realpath( os.path.join( repo_directory, 'validator' ) )
	out_dir = os.path.realpath(out_dir)

	SetupOutDir(out_dir)
	GenValidatorProtoascii(validator_directory, out_dir)
	GenValidatorPb2Py(validator_directory, out_dir)
	GenValidatorProtoascii(validator_directory,out_dir)
	GeneratePHP(repo_directory, out_dir)

if __name__ == '__main__':
	if len( sys.argv ) == 0:
		Die( "Error: Must supply amphtml directory as first argument" )
	repo_directory = sys.argv[1]
	if not os.path.exists( repo_directory ):
		Die( "Error: The amphtml directory does not exist: %s" % validator_directory )
	repo_directory = os.path.realpath( repo_directory )
	out_dir = os.path.join( tempfile.gettempdir(), 'amp_wp' )
	Main( repo_directory, out_dir )
