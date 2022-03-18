<?php

namespace AmpProject\AmpWP\Tests\PairedUrlStructure;

use AmpProject\AmpWP\PairedUrlStructure\LegacyTransitionalUrlStructure;
use AmpProject\AmpWP\Tests\DependencyInjectedTestCase;

/** @coversDefaultClass \AmpProject\AmpWP\PairedUrlStructure\LegacyTransitionalUrlStructure */
class LegacyTransitionalUrlStructureTest extends DependencyInjectedTestCase {

	/** @var LegacyTransitionalUrlStructure */
	private $instance;

	public function set_up() {
		parent::set_up();
		$this->instance = $this->injector->make( LegacyTransitionalUrlStructure::class );
	}

	/** @covers ::add_endpoint() */
	public function test_add_endpoint() {
		$slug = amp_get_slug();
		$this->assertEquals(
			home_url( "/foo/?{$slug}" ),
			$this->instance->add_endpoint( home_url( '/foo/' ) )
		);
	}

	/** @covers ::has_endpoint() */
	public function test_has_endpoint() {
		$slug = amp_get_slug();
		$this->assertFalse( $this->instance->has_endpoint( home_url( '/foo/' ) ) );
		$this->assertTrue( $this->instance->has_endpoint( home_url( "/foo/?{$slug}" ) ) );
	}

	/** @covers ::remove_endpoint() */
	public function test_remove_endpoint() {
		$slug = amp_get_slug();
		$this->assertEquals(
			home_url( '/foo/' ),
			$this->instance->remove_endpoint( home_url( "/foo/?{$slug}" ) )
		);
	}
}
