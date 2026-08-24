"""The three route owner modules are the only route modules registered by the app."""

from pathlib import Path


def test_main_registers_the_three_route_owner_modules():
    import inspect

    from chronos import main
    from chronos.api_routes_advisor import router as advisor_router
    from chronos.api_routes_investor import router as investor_router
    from chronos.api_routes_system import router as system_router

    for router in (investor_router, advisor_router, system_router):
        assert router.routes

    source = inspect.getsource(main)
    assert source.count("app.include_router(") == 3
    assert "app.include_router(api_routes_system.router)" in source
    assert "app.include_router(api_routes_investor.router)" in source
    assert "app.include_router(api_routes_advisor.router)" in source


def test_legacy_compatibility_packages_are_absent():
    chronos_root = Path(__file__).resolve().parents[1] / "chronos"
    legacy_package_names = {
        "advisor_workspace",
        "api_routes",
        "app_startup",
        "demo_users",
        "investor_accounts",
        "investor_trading",
        "market_data_setup",
        "market_price_queries",
        "portfolio_performance",
        "shared_database",
        "simulation_clock",
    }

    assert not any((chronos_root / package_name).exists() for package_name in legacy_package_names)
