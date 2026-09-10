//-----------------------------------------------------------------------------
// Sigil II optional spider. Vanilla SpiderMastermind is 3000 HP.
// E6M8 is the only Sigil II map that should use this.
//-----------------------------------------------------------------------------

class SpiderMastermindSigil2 : SpiderMastermind
{
    Default
    {
        Tag "Sigil II Spider Mastermind";
        Health 9000;
        PainChance 20;
        Speed 14;
        FastSpeed 18;
        Mass 1200;
        +BOSS
        +BOSSDEATH
        +NORADIUSDMG
        +DONTMORPH
        +MISSILEMORE
        +MISSILEEVENMORE
        +NOICEDEATH
    }
}