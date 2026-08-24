"""The three route owner modules are the only route modules registered by the app."""


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


def test_legacy_route_modules_only_export_their_owner_router():
    from chronos.api_routes import (
        advisor_workspace_routes,
        demo_user_routes,
        investor_account_routes,
        investor_trade_routes,
        market_price_routes,
        simulation_clock_routes,
    )
    from chronos.api_routes_advisor import router as advisor_router
    from chronos.api_routes_investor import router as investor_router
    from chronos.api_routes_system import router as system_router

    assert advisor_workspace_routes.router is advisor_router
    assert demo_user_routes.router is system_router
    assert simulation_clock_routes.router is system_router
    assert investor_account_routes.router is investor_router
    assert investor_trade_routes.router is investor_router
    assert market_price_routes.router is investor_router
