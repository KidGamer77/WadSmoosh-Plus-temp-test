//-----------------------------------------------------------------------------
// Remnants of Earth — JE4_MAP08 only.
// wadsmoosh.py already rewrites editor number 3115 -> 32000 so decorate
// CyberMastermind spawns instead of the ID24 hanging torso (DEH Thing 181).
// This handler is a one-shot safety net for maps that still place a
// vanilla Spider Mastermind (doomednum 7). It must NEVER invent a boss
// on a blood floor and must NEVER run every tic.
//-----------------------------------------------------------------------------

class JE4BossFix : EventHandler
{
    private bool done;

    override void WorldLoaded(WorldEvent e)
    {
        done = false;

        if (!(level.MapName ~== "JE4_MAP08"))
            return;

        ReplaceIfNeeded();
        done = true;
    }

    override void WorldTick()
    {
        // First few tics only, in case the thing is spawned by a script
        // after WorldLoaded. Never loop for the whole map.
        if (done)
            return;
        if (!(level.MapName ~== "JE4_MAP08"))
            return;
        if (level.maptime < 1 || level.maptime > 8)
            return;

        ReplaceIfNeeded();
        done = true;
    }

    private void ReplaceIfNeeded()
    {
        if (FindFirst("CyberMastermind"))
            return;

        Array<Actor> victims;
        CollectClass("SpiderMastermind", victims);

        int replaced = 0;
        for (int i = 0; i < victims.Size(); i++)
        {
            Actor old = victims[i];
            if (!old) continue;

            let boss = Actor.Spawn("CyberMastermind", old.pos, ALLOW_REPLACE);
            if (boss)
            {
                boss.angle = old.angle;
                boss.A_SetHealth(boss.SpawnHealth());
                replaced++;
            }
            old.Destroy();
        }

        // If the Python rewrite already placed 32000, victims is empty
        // and we do nothing. Do not spawn a fallback boss.
        replaced = replaced;
    }

    private Actor FindFirst(string cls)
    {
        let it = ThinkerIterator.Create(cls);
        return Actor(it.Next());
    }

    private void CollectClass(string cls, out Array<Actor> dest)
    {
        let it = ThinkerIterator.Create(cls);
        Actor mo;
        while ((mo = Actor(it.Next())))
            dest.Push(mo);
    }
}