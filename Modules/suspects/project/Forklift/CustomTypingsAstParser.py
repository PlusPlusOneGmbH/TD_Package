
'''Info Header Start
Name : typingsAstParser
Author : Wieland PlusPlusOne@AMB-ZEPH15
Saveorigin : Project.toe
Saveversion : 2023.31378
Info Header End'''
# This is fucking something up real hard here. WTF?
# from ast import *
from ast import ClassDef, Name, Expr, AnnAssign, ImportFrom, alias, Load, Pass, Subscript, Module, unparse,Store, FunctionDef, Raise, arguments, arg, Tuple, Call, If, Constant

def customParTree(targetComp:COMP):
    return ClassDef(
        name='CustomPars',
        bases=[
            Name(id='ParCollection', ctx=Load())],
            keywords=[],
        body=sum( [
            [
                AnnAssign(
                    target=Name(id=customPar.name, ctx=Store()),
                    annotation=Name(id=f'Par{customPar.style}', ctx=Load()),
                    simple=1),
                Expr( value = Name('"""', ctx = Load())),
                Expr( value = Name(f'{customPar.help}', ctx = Load())),
                Expr( value = Name(f'Parameter Page : {customPar.page}', ctx = Load())),
                Expr( value = Name('"""', ctx = Load()))
            ]  for customPar in targetComp.customPars
        ], []),
        decorator_list=[]
    )

def importExtensions( targetComp:COMP ):
    moduleName = "/".join( op(targetComp).relativePath( op( targetComp.extensions[0].__module__ ) ).split("/")[1:] )
    return [
        ImportFrom(
            f".{moduleName}",
            names = [
                alias( name = extension.__class__.__name__ )
            ]
        ) for extension in targetComp.extensions
    ] 

def importCompPars( targetComp:COMP):
    opType = targetComp.OPType[0].upper() + targetComp.OPType[1:]
    
    return ImportFrom(
        module=f'tdi.ops.{targetComp.family.lower()}s.{targetComp.OPType}',
        names=[
            alias(name=f'{opType }Pars', asname="opPars")],
        level=0)
        
       
def createTypingTree( targetComp:COMP):
    return [
        ImportFrom(
            module='typing',
            names=[ 
                alias(name='Union')
            ], level=0
        ),
        *importExtensions( targetComp ),
        importCompPars( targetComp ),
        ImportFrom( module='tdi.parTypes', names=[ alias(name='*')], level=0),
        customParTree( targetComp),
        ClassDef(
            name='Typing',
            bases=
                [ Name(id=extension.__class__.__name__, ctx=Load()) for extension in targetComp.extensions ] +
                [ Name(id=targetComp.opType, ctx=Load()) ]
            ,
            keywords=[],
            decorator_list=[],
            body=[
                AnnAssign(
                    target=Name(id='par', ctx=Store()),
                    annotation=Subscript(
                        value=Name(id='Union', ctx=Load()),
                        slice=Tuple(
                            elts=[
                                Name(id='opPars', ctx=Load()),
                                Name(id='CustomPars', ctx=Load())],
                            ctx=Load()),
                        ctx=Load()),
                    simple=1),
                        Pass()]
        )
    ]

def createDefaultTypingClass():
    return ClassDef(
                    name='Typing',
                    bases=[],
                    keywords=[],
                    body=[
                        FunctionDef(
                            name='__getattribute__',
                            lineno = 0,
                            args=arguments(
                                posonlyargs=[],
                                args=[
                                    arg(arg='self'),
                                    arg(arg='name')],
                                kwonlyargs=[],
                                kw_defaults=[],
                                defaults=[]),
                            body=[
                                Raise(
                                    exc=Call(
                                        func=Name(id='NotImplemented', ctx=Load()),
                                        
                                        args=[
                                            Constant(value='This Class is only for Typehinting!')],
                                        keywords=[]))],
                            decorator_list=[])],
                    decorator_list=[])

def createTypingModuleTree( targetComp:COMP):
    return Module(
    body=[
        ImportFrom(
            module='typing',
            names=[
                alias(name='TYPE_CHECKING')],
            level=0),
        If(
            test=Name(id='TYPE_CHECKING', ctx=Load()),
            body=createTypingTree( targetComp ),
            orelse=[
                createDefaultTypingClass()
                ])],
    type_ignores=[])

def createTypingModuleString( targetComp:COMP):
    return unparse( createTypingModuleTree( targetComp ))

