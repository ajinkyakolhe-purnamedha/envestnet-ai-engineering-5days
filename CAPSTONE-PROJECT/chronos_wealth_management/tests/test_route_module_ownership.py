"""The three route owner modules are the only route modules registered by the app."""


def test_main_registers_the_three_route_owner_modules():
    from chronos import main
    from chronos.api_routes_advisor import router as advisor_router
    from chronos.api_routes_investor import router as investor_router
    from chronos.api_routes_system import router as system_router

    assert main.app.router.routes
    for router in (investor_router, advisor_router, system_router):
        assert router.routes

    assert sum(type(route).__name__ == "_IncludedRouter" for route in main.app.routes) == 3


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
