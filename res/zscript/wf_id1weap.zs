//-----------------------------------------------------------------------------
// UZDoom 5.x LoR / ID24 weapon swap.
// Do not define Incinerator / Heatwave / Fuel here.
// Missing ID24 classes must not VM-abort.
//-----------------------------------------------------------------------------

class Id1WeaponHandler : EventHandler
{
    private int WeapSwapMode()
    {
        let cv = CVar.FindCVar("wf_id1_weapswap");
        if (cv == null) return 1;
        return cv.GetInt();
    }

    private bool ShouldSwap()
    {
        int mode = WeapSwapMode();
        if (mode <= 0) return false;
        if (mode >= 2) return true;

        string mapName = Level.MapName.MakeLower();
        string prefix = mapName.Left(3);
        return (prefix == "lr_" || prefix == "dm_");
    }

    private class<Actor> FindActorClass(Name n)
    {
        class<Actor> cls = n;
        return cls;
    }

    override void CheckReplacement(ReplaceEvent e)
    {
        if (e.Replacee == null) return;
        if (!ShouldSwap()) return;

        let incinerator = FindActorClass("ID24Incinerator");
        let blade = FindActorClass("ID24CalamityBlade");
        let fuel = FindActorClass("ID24Fuel");
        let tank = FindActorClass("ID24FuelTank");

        if (e.Replacee == "PlasmaRifle")
        {
            if (incinerator) e.Replacement = incinerator;
        }
        else if (e.Replacee == "BFG9000")
        {
            if (blade) e.Replacement = blade;
        }
        else if (e.Replacee == "Cell")
        {
            if (fuel) e.Replacement = fuel;
        }
        else if (e.Replacee == "CellPack")
        {
            if (tank) e.Replacement = tank;
        }
    }
}